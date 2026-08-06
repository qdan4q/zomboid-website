from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import UserProfile
from core.models import SiteSettings
from marketplace.models import MarketplaceListing
from news.models import NewsArticle


class Command(BaseCommand):
    help = ""

    @staticmethod
    def find_seeded_user(user_model, russian_username, old_username):
        return user_model.objects.filter(
            username__in=[russian_username, old_username]
        ).first()

    @transaction.atomic
    def handle(self, *args, **options):
        user_model = get_user_model()
        admin = self.find_seeded_user(user_model, "администратор", "admin")
        if admin is None:
            admin = user_model(username="администратор")
        admin.username = "администратор"
        admin.email = ""
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.set_password("НоксАдмин!1993")
        admin.save()

        survivor_profiles = [
            (
                "выживший1",
                "survivor1",
                "Мара Пайк",
                "Плотник",
                "alive",
                "Поддерживает западный ретранслятор с помощью найденной проволоки и старых деталей.",
            ),
            (
                "выживший2",
                "survivor2",
                "Элиас Уорд",
                "Фельдшер",
                "injured",
                "Содержит пункт первой помощи за старым складом кормов.",
            ),
            (
                "выживший3",
                "survivor3",
                "Джун Мерсер",
                "Радист",
                "alive",
                "Слушает гражданские частоты и записывает необычные передачи.",
            ),
            (
                "выживший4",
                "survivor4",
                "Тео Белл",
                "Механик",
                "missing",
                "Последний раз его видели у брошенной колонны к северу от Малдро.",
            ),
            (
                "выживший5",
                "survivor5",
                "Рут Колдер",
                "Собиратель",
                "unknown",
                "Отмечает безопасные колодцы, огороды и тихие пути между поселениями.",
            ),
        ]
        survivors = []
        for russian_username, old_username, character, occupation, status, biography in survivor_profiles:
            user = self.find_seeded_user(user_model, russian_username, old_username)
            if user is None:
                user = user_model(username=russian_username)
            user.username = russian_username
            user.email = ""
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.set_password("Выживший!1993")
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.character_name = character
            profile.occupation = occupation
            profile.status = status
            profile.biography = biography
            profile.save()
            survivors.append(user)

        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "website_name": "Общественная сеть Нокса",
                "welcome_message": "Добровольный узел связи для выживших внутри закрытой зоны Нокс.",
                "emergency_message": "Берегите чистую воду. Не приближайтесь к заражённым, которые подают друг другу знаки.",
                "server_status": "В СЕТИ — сигнал нестабилен",
            },
        )

        public_articles = [
            (
                "Правительство заявляет, что ситуация в Кентукки под контролем",
                "Government Claims the Kentucky Situation Is Contained",
                "world",
                "Национальные передачи утверждают, что граница закрытой зоны по-прежнему надёжна, несмотря на перебои связи.",
                "Федеральный диктор повторил, что города за пределами Кентукки продолжают работу, а колонны помощи уже формируются. Передача оборвалась, когда позвонивший спросил, почему два северных поста перестали выходить на связь. Местные наблюдатели советуют считать все официальные маршруты устаревшими.",
            ),
            (
                "Неизвестный радиосигнал обнаружен возле Вест-Пойнта",
                "Unknown Radio Signal Detected Near West Point",
                "radio",
                "После полуночи под гражданской аварийной частотой услышали повторяющуюся последовательность.",
                "Операторы ретранслятора К-12 записали три тона, после которых голос перечислял названия улиц в обратном порядке. Ни одна известная группа выживших не признала сигнал своим. Последняя передача закончилась словами «они ждут света», после чего несущая исчезла.",
            ),
            (
                "Военная колонна не добралась до Луисвилла",
                "Military Convoy Fails to Reach Louisville",
                "military",
                "Колонна снабжения, которую ждали у северной карантинной линии, опаздывает уже на двенадцать часов.",
                "Сначала на дальней военной частоте сообщили о повреждённых дорогах, затем потребовали, чтобы гражданские покинули канал. Над западной трассой 31 заметили дым. Всем, кто находится рядом, следует укрыться и избегать машин с неподтверждёнными знаками подразделений.",
            ),
            (
                "Выжившие сообщают, что заражённые открывают двери",
                "Survivors Report Infected Opening Doors",
                "rumor",
                "Три не связанных между собой свидетеля видели, как заражённые проверяли дверные ручки перед входом.",
                "Сообщения пришли из Риверсайда, с фермы южнее Доу-Вэлли и с одинокой заправки. Свидетели не знают, вспомнили ли заражённые это действие или повторяли за живыми людьми. Запирайте и укрепляйте двери, даже если снаружи нет движения.",
            ),
            (
                "Исследовательская группа пропала возле закрытого объекта",
                "Research Team Disappears Near Restricted Facility",
                "scientific",
                "Университетская полевая группа перестала отвечать вскоре после запроса военной эвакуации.",
                "В последнем открытом сообщении исследователи упомянули группы заражённых, которые уходили от громкого шума, а не шли к нему. Власти отрицают, что в зону входила утверждённая научная группа. Их переносной маяк каждые шесть минут передаёт пустой пакет данных.",
            ),
            (
                "Водоснабжение признано небезопасным",
                "Water Supply Declared Unsafe",
                "knox",
                "Мутный сток попал в несколько колодцев к востоку от железнодорожной станции.",
                "Кипятите собранную воду не менее минуты и выливайте всё, что пахнет химикатами. Старые городские насосы отключены. Добровольцы проверят отмеченные колодцы, когда появятся реактивы; до этого не доверяйте официальным синим меткам безопасности.",
            ),
            (
                "Поведенческий отчёт КН-17",
                "Behavioral Report KX-17",
                "scientific",
                "Наблюдатели подтверждают небольшие изменения в реакции некоторых заражённых на преграды и звук.",
                "В открытой сводке отмечены повторяющиеся обходы, остановки у запертых входов и внимание к жестам других заражённых. Причина не установлена. Соблюдайте обычные меры предосторожности и сообщайте о закономерностях, не приближаясь для проверки.",
            ),
            (
                "Установлена новая карантинная линия",
                "New Quarantine Line Established",
                "world",
                "Военные передачи объявили о втором периметре сдерживания далеко за пределами округа Нокс.",
                "В объявлении новую линию называют временной мерой снабжения и отрицают заражение за пределами Кентукки. Гражданский транспорт перенаправляют в обход нескольких неназванных городов. Коротковолновые станции севернее всю ночь слышали тяжёлые самолёты.",
            ),
        ]
        restricted_articles = [
            (
                "КН-17: подтверждена способность решать задачи",
                "KX-17: Confirmed Problem-Solving Behavior",
                "scientific",
                "Закрытые наблюдения показывают поведение, которое уже нельзя считать случайностью.",
                "Плёнка со станции КН-17 показывает, как заражённый подвинул стул к разбитому окну, а затем вернулся с двумя другими. После восстановления комнаты последовательность повторилась. Командование приказало запечатать все копии и переписать открытую сводку как неподтверждённое наблюдение.",
            ),
            (
                "Потеряна связь с исследовательской станцией",
                "Loss of Contact with Research Station",
                "scientific",
                "Подземная группа пропустила два сеанса связи после сообщения о нарушении изоляции.",
                "С хребта всё ещё видно резервное освещение, однако автоматика двери регистрирует повторные попытки доступа изнутри. Спасателям приказано ждать военный конвой, который так и не прибыл. Координаты станции не разглашать.",
            ),
            (
                "Приказ подавлять гражданские радиопередачи",
                "Orders to Suppress Civilian Radio Broadcasts",
                "military",
                "Кодированная директива называет независимые передатчики угрозой контролю периметра.",
                "Подразделениям приказано изымать мощное оборудование, а перебои объяснять разрушением инфраструктуры. В директиве отдельно перечислены добровольческие погодные и медицинские ретрансляторы. К-12 пока не назван, но операторам следует сократить время выхода в эфир.",
            ),
            (
                "Возможное заражение за пределами Кентукки",
                "Possible Infection Outside Kentucky",
                "world",
                "Два перехваченных медицинских сообщения описывают совпадающие симптомы в северном транспортном узле.",
                "Ни один пациент не проезжал через периметр Нокса. В более позднем сообщении диагноз заменили на воздействие промышленных веществ и убрали имя лечащего врача. До подтверждения отчёт остаётся доступным только администраторам сети.",
            ),
        ]

        all_articles = public_articles + restricted_articles
        for offset, (title, old_title, news_type, summary, content) in enumerate(all_articles):
            visibility = (
                NewsArticle.Visibility.SURVIVORS
                if offset < len(public_articles)
                else NewsArticle.Visibility.ADMIN_ONLY
            )
            article = NewsArticle.objects.filter(title__in=[title, old_title]).first()
            if article is None:
                article = NewsArticle(title=title)
            article.title = title
            article.summary = summary
            article.content = content
            article.news_type = news_type
            article.visibility = visibility
            article.author = admin
            article.in_game_date = date(1993, 7, 9 + offset)
            article.save()
            NewsArticle.objects.filter(title=old_title).exclude(pk=article.pk).delete()

        listing_data = [
            ("Два ящика чистых банок", "Two boxes of clean jars", "for_sale", "Неиспользованные банки, завёрнутые в газету.", "Три банки еды", "Ферма к западу от города", "Спросить Мару на шестом канале", "active"),
            ("Срочно нужны антибиотики", "Antibiotics urgently wanted", "wanted", "Нужен запечатанный курс для наблюдаемой заражённой раны.", "Топливо, батарейки или ремонт", "Медпункт у старого склада кормов", "Оставить красную ткань на боковых воротах", "active"),
            ("Обмен: рабочий коротковолновый приёмник", "Trade: working shortwave receiver", "trade", "Приёмник работает от батарей; ручка настройки заедает.", "Хороший топор и ламповое масло", "Ретранслятор К-12", "Вызывать Джун после 20:00", "active"),
            ("Ремонт автомобилей", "Vehicle repairs", "services", "Простой ремонт двигателя, колёс и сварка, если принесёте детали.", "Еда или треть найденного топлива", "Южный гараж", "Отметить внешний забор белым мелом", "active"),
            ("Огородной бригаде нужны двое", "Garden crew seeking two hands", "group_recruitment", "Дневная работа: вскопать землю и укрепить ограду.", "Доля урожая", "Общий огород возле церкви", "Встретить Рут в полдень", "active"),
            ("ПРЕДУПРЕЖДЕНИЕ: шум у железной дороги", "WARNING: noise near rail yard", "warning", "После заката слышны повторяющиеся удары металла; сигналов выживших не видно.", "Только информация", "Восточная железнодорожная станция", "Дополнить запись на доске после проверки", "active"),
            ("Запасные бочки для дождевой воды", "Spare rain barrels", "for_sale", "Две целые пластиковые бочки с плотно закрывающимися крышками.", "Ручная пила или четыре коробки гвоздей", "Домики у северной границы", "Третий радиоканал", "active"),
            ("Карты тихих сельских дорог", "Maps of quiet farm roads", "other", "Копии маршрутов с отмеченными колодцами и разрушенными мостами.", "Свежие батарейки", "Передвижной обменный пункт", "Спросить у ретранслятора К-12", "active"),
            ("Набор деталей для генератора", "Generator parts bundle", "trade", "Ремни, свечи и один очищенный карбюратор.", "Обменяно на медицинскую марлю", "Южный гараж", "Объявление завершено", "sold"),
            ("Сопровождение через Риверсайд", "Escort through Riverside", "services", "Прежнее предложение дневного сопровождения двумя людьми.", "Предложение отозвано", "Граница Риверсайда", "Связи нет", "closed"),
        ]
        for index, (title, old_title, category, description, trade, location, contact, status) in enumerate(listing_data):
            owner = survivors[index % len(survivors)]
            listing = MarketplaceListing.objects.filter(title__in=[title, old_title]).first()
            if listing is None:
                listing = MarketplaceListing(title=title)
            listing.title = title
            listing.description = description
            listing.category = category
            listing.author = owner
            listing.character_name = owner.profile.character_name
            listing.price_or_trade = trade
            listing.meeting_location = location
            listing.contact_information = contact
            listing.status = status
            listing.save()
            MarketplaceListing.objects.filter(title=old_title).exclude(pk=listing.pk).delete()
