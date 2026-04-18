import csv
import random
import asyncio
import logging
from pathlib import Path
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import UserPrivacyRestrictedError, UserNotMutualContactError, EntityNotFoundError

import config

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def add_members(client, target_group_identifier: str) -> int:
    """
    إضافة الأعضاء إلى جروب آخر مع التسجيل
    
    Args:
        client: Telegram client
        target_group_identifier: اسم الجروب أو ID المستهدف
    
    Returns:
        عدد الأعضاء المضافين بنجاح
    """
    
    # ✅ تحقق من وجود ملف الأعضاء
    if not Path(config.MEMBERS_FILE).exists():
        logger.error(f"❌ الملف {config.MEMBERS_FILE} غير موجود. قم بـ scrape الأعضاء أولاً!")
        return 0

    try:
        target_group = await client.get_entity(target_group_identifier)
        logger.info(f"✅ تم الاتصال بجروب الهدف: {target_group.title}")
    except EntityNotFoundError:
        logger.error(f"❌ لم يتم العثور على الجروب: {target_group_identifier}")
        return 0
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال: {str(e)}")
        return 0

    added_count = 0
    failed_count = 0
    added_list = []

    try:
        with open(config.MEMBERS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            # ✅ تعامل مع الملفات بدون headers
            if reader.fieldnames is None or reader.fieldnames[0] != "username":
                f.seek(0)
                reader = csv.reader(f)
                usernames = [row[0] for row in reader if row]
            else:
                usernames = [row.get("username") for row in reader if row.get("username")]

        total = len(usernames)
        logger.info(f"📋 عدد الأعضاء للإضافة: {total}")

        for idx, username in enumerate(usernames, 1):
            try:
                logger.info(f"[{idx}/{total}] 👤 جاري إضافة @{username}...")
                
                user = await client.get_entity(username)
                
                await client(
                    InviteToChannelRequest(
                        channel=target_group,
                        users=[user]
                    )
                )

                added_count += 1
                added_list.append(username)
                logger.info(f"✅ تمت إضافة @{username} بنجاح")

                # ✅ تأخير عشوائي لتجنب الحظر
                delay = random.randint(config.ADD_DELAY_MIN, config.ADD_DELAY_MAX)
                logger.info(f"⏳ انتظار {delay}s...")
                await asyncio.sleep(delay)

            except UserPrivacyRestrictedError:
                logger.warning(f"⚠️ @{username} - إعدادات الخصوصية تمنع الإضافة")
                failed_count += 1
                
            except UserNotMutualContactError:
                logger.warning(f"⚠️ @{username} - لا يمكن إضافة دون أن يكون متابع")
                failed_count += 1
                
            except EntityNotFoundError:
                logger.warning(f"⚠️ @{username} - المستخدم غير موجود")
                failed_count += 1
                
            except Exception as e:
                logger.error(f"❌ @{username} - خطأ: {str(e)}")
                failed_count += 1

        # ✅ حفظ الأعضاء المضافين بنجاح
        try:
            with open(config.ADDED_MEMBERS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["username", "status"])
                for username in added_list:
                    writer.writerow([username, "added"])
            
            logger.info(f"✅ تم حفظ النتائج في {config.ADDED_MEMBERS_FILE}")
            
        except IOError as e:
            logger.error(f"❌ خطأ في حفظ النتائج: {str(e)}")

        logger.info(f"\n{'='*50}")
        logger.info(f"📊 النتائج النهائية:")
        logger.info(f"   ✅ تمت إضافتهم: {added_count}")
        logger.info(f"   ❌ فشل: {failed_count}")
        logger.info(f"   📝 المجموع: {total}")
        logger.info(f"{'='*50}\n")

        return added_count

    except FileNotFoundError:
        logger.error(f"❌ لم يتم العثور على الملف {config.MEMBERS_FILE}")
        return 0
    except Exception as e:
        logger.error(f"❌ خطأ عام: {str(e)}")
        return 0
