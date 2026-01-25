from datetime import date
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, MoodRecord

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