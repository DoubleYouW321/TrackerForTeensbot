from datetime import date
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, MoodRecord, Homework, HomeworkProgress, DailyMetric, Category, Comment

#Добавление пользователя
async def req_set_user(session: AsyncSession, data: int):
    result = await session.execute(
        select(User).where(User.tg_id == data)
    )
    user = result.scalar_one_or_none()
        
    if user:
        await session.commit()
        return user
    else:
        user = User(tg_id=data)
        session.add(user)
        await session.commit()
        return user

# запросы для дневника настроения
async def req_save_mood_record(session: AsyncSession, tg_id: int, mood_type: str, emoji: str):
        user = await req_set_user(session, tg_id)
        today_str = date.today().isoformat()
        
        mood_record = MoodRecord(
            user_id=user.id,
            date=today_str,
            mood=mood_type,
            emoji=emoji
        )
        session.add(mood_record)
        await session.commit()
        return mood_record

async def req_get_mood_statistics(session: AsyncSession, tg_id: int):
        user = await req_set_user(session, tg_id)
        
        result = await session.execute(
            select(
                MoodRecord.mood,
                MoodRecord.emoji,
                func.count(MoodRecord.id).label('count')
            )
            .where(MoodRecord.user_id == user.id)
            .group_by(MoodRecord.mood, MoodRecord.emoji)
            .order_by(func.count(MoodRecord.id).desc())
        )
        
        stats = result.all()
        
        if not stats:
            return None
        
        total_count = sum(stat.count for stat in stats)
        return {
            'total': total_count,
            'stats': [
                {'mood': stat.mood, 'emoji': stat.emoji, 'count': stat.count}
                for stat in stats
            ],
            'most_common': {
                'mood': stats[0].mood,
                'emoji': stats[0].emoji,
                'count': stats[0].count
            }
        }

async def req_get_all_moods(session: AsyncSession, tg_id: int):
    user = await req_set_user(session, tg_id)
        
    result = await session.execute(
        select(MoodRecord)
        .where(MoodRecord.user_id == user.id)
        .order_by(MoodRecord.date.desc(), MoodRecord.id.desc())
        )
        
    moods = result.scalars().all()
    return [
        {
            'date': mood.date,
            'emoji': mood.emoji,
            'mood': mood.mood
        }
        for mood in moods
    ]

# запросы для ДЗ

async def req_add_homework(session: AsyncSession, data: dict):
    obj = Homework(
        tg_id=data['tg_id'],
        lesson=data['lesson'],
        description=data['description'],
        deadline=data['deadline'],
    )
    session.add(obj)
    await session.commit()

async def req_get_my_homeworks(session: AsyncSession, tg_id: int):
    await delete_expired_homeworks(session, tg_id)
    
    query = select(Homework).where(
        Homework.tg_id == tg_id
    ).order_by(Homework.deadline)
    result = await session.execute(query)
    return result.scalars().all()

async def req_delete_homework(session: AsyncSession, homework_id: int):
    query = delete(Homework).where(Homework.id == homework_id)
    await session.execute(query)
    await session.commit()

async def req_update_homework_progress(session: AsyncSession, tg_id: int, is_expired: bool = False):
    query = select(HomeworkProgress).where(HomeworkProgress.tg_id == tg_id)
    result = await session.execute(query)
    progress = result.scalar_one_or_none()
    
    if progress:
        if is_expired:
            progress.expired_count += 1
        else:
            progress.completed_count += 1
    else:
        if is_expired:
            progress = HomeworkProgress(
                tg_id=tg_id,
                expired_count=1,
                completed_count=0
            )
        else:
            progress = HomeworkProgress(
                tg_id=tg_id,
                completed_count=1,
                expired_count=0
            )
        session.add(progress)
    
    await session.commit()
    return progress

async def req_get_homework_progress(session: AsyncSession, tg_id: int):
    query = select(HomeworkProgress).where(HomeworkProgress.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def delete_expired_homeworks(session: AsyncSession, tg_id: int):
    today = date.today()
    
    query = select(Homework).where(
        and_(
            Homework.tg_id == tg_id,
            Homework.deadline < today
        )
    )
    result = await session.execute(query)
    expired_homeworks = result.scalars().all()
    
    for homework in expired_homeworks:
        delete_query = delete(Homework).where(Homework.id == homework.id)
        await session.execute(delete_query)
        
        await req_update_homework_progress(session, tg_id, is_expired=True)
    
    await session.commit()
    return expired_homeworks

# Запросы для ДЗ

async def req_save_daily_metrics(session: AsyncSession, tg_id: int, water: int, sleep: float, steps: int):
    user = await req_set_user(session, tg_id)
    today_str = date.today().isoformat()
        
    metric = await session.scalar(
    select(DailyMetric).where(
            and_(DailyMetric.tg_id == user.tg_id, DailyMetric.date == today_str)
        )
    )
        
    if metric:
        metric.water_glasses = water
        metric.sleep_hours = sleep
        metric.steps = steps
    else:
        metric = DailyMetric(
            tg_id=user.tg_id,
            date=today_str,
            water_glasses=water,
            sleep_hours=sleep,
            steps=steps
        )
        session.add(metric)
        
    await session.commit()
        
    return {
        'water_glasses': water,
        'sleep_hours': sleep,
        'steps': steps,
        'date': today_str
    }

async def req_get_today_metrics(session: AsyncSession, tg_id: int):
    user = await req_set_user(session, tg_id)
    today_str = date.today().isoformat()
        
    metric = await session.scalar(
        select(DailyMetric).where(
            and_(DailyMetric.tg_id == user.tg_id, DailyMetric.date == today_str)
        )
    )
        
    if metric:
        return {
            'water_glasses': metric.water_glasses,
            'sleep_hours': metric.sleep_hours,
            'steps': metric.steps,
            'date': metric.date
        }
    return None

async def req_get_user_category(session: AsyncSession, tg_id: int):
    user = await req_set_user(session, tg_id)
    
    result = await session.execute(
        select(Category).where(Category.tg_id == tg_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        category = Category(
            tg_id=tg_id,
            water=8,      
            hours=8,      
            steps=10000   
        )
        session.add(category)
        await session.commit()
    
    return {
        'water': category.water,
        'hours': category.hours,
        'steps': category.steps
    }

# Запросы для фидбэка

async def req_set_comment(session: AsyncSession, tg_id, comment_text):
    try:
        session.add(Comment(tg_id=tg_id, comment_text=comment_text))
        await session.commit()
    except Exception as e:
        print(f"Ошибка при сохранении комментария: {e}")