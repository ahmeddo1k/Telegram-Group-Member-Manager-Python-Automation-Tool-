import csv
import logging
from typing import List
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import EntityNotFoundError

import config

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def scrape_members(client, group_identifier: str) -> List[str]:
    """
    استخراج أعضاء الجروب وحفظهم في CSV
    
    Args:
        client: Telegram client
        group_identifier: اسم الجروب أو ID
    
    Returns:
        قائمة أسماء المستخدمين
    """
    try:
        # الحصول على entity الجروب
        group = await client.get_entity(group_identifier)
        logger.info(f"✅ تم الاتصال بالجروب: {group.title}")
        
    except EntityNotFoundError:
        logger.error(f"❌ لم يتم العثور على الجروب: {group_identifier}")
        return []
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال: {str(e)}")
        return []

    members = []
    offset = 0
    limit = 200  # ✅ Telethon يدعم حد أقصى 200 في الطلب الواحد
    total_members = 0

    try:
        while True:
            logger.info(f"📥 جاري استخراج الأعضاء (offset: {offset})...")
            
            participants = await client(
                GetParticipantsRequest(
                    channel=group,
                    filter=ChannelParticipantsSearch(""),
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )

            # إذا لم يكن هناك نتائج، توقف الحلقة
            if not participants.users:
                break

            for user in participants.users:
                # ✅ تحقق من وجود username وتجنب الحسابات الخاصة
                if user.username:
                    members.append(user.username)
                    total_members += 1

            offset += limit

            # معالجة الحد الأقصى للطلبات
            if len(participants.users) < limit:
                break

        logger.info(f"✅ تم استخراج {total_members} عضو")

        # ✅ حفظ في CSV مع معالجة الأخطاء
        try:
            with open(config.MEMBERS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["username"])  # ✅ أضفنا header
                for m in members:
                    writer.writerow([m])
            
            logger.info(f"✅ تم حفظ {len(members)} عضو في {config.MEMBERS_FILE}")
            
        except IOError as e:
            logger.error(f"❌ خطأ في حفظ الملف: {str(e)}")
            return []

        return members

    except Exception as e:
        logger.error(f"❌ خطأ عام: {str(e)}")
        return []
