"""Create a polished, repeatable demo dataset for Coderr."""

from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from profile_app.models import Profile
from reviews_app.models import Review


BUSINESSES = [
    ("kevin", "asdasd24", "Kevin", "Alpha", "kevin@example.com", "Rostock", "015123456789", "Fullstack Developer mit Fokus auf moderne Webanwendungen.", "In der Woche", "#00b67a"),
    ("demo_design", "Demo123!", "Sofia", "Brandt", "sofia@example.com", "Hamburg", "040 555 0182", "Brand Designerin fuer klare Marken und starke visuelle Auftritte.", "Mo-Fr, 9-17 Uhr", "#7457d9"),
    ("demo_marketing", "Demo123!", "Mira", "Wolf", "mira@example.com", "Berlin", "030 555 0148", "Content- und Social-Media-Strategien fuer wachsende Unternehmen.", "Mo-Sa, flexibel", "#e46b3c"),
    ("demo_video", "Demo123!", "Jonas", "Klein", "jonas@example.com", "Koeln", "0221 555 0164", "Video Editor und Motion Designer fuer Social Media und Werbung.", "Mo-Fr, 10-18 Uhr", "#2878d0"),
]

CUSTOMERS = [
    ("andrey", "asdasd", "Andrey", "Koch", "andrey@example.com", "Muenchen", "Gruender eines jungen E-Commerce-Unternehmens.", "#1f9d75"),
    ("demo_customer_lena", "Demo123!", "Lena", "Hoffmann", "lena@example.com", "Leipzig", "Betreibt ein lokales Cafe und einen kleinen Onlineshop.", "#c75b7a"),
    ("demo_customer_tim", "Demo123!", "Tim", "Neumann", "tim@example.com", "Dresden", "Produktmanager mit regelmaessigem Bedarf an Kreativleistungen.", "#d19a2a"),
]

OFFERS = [
    ("kevin", "Moderne Business-Website entwickeln", "Responsive Website mit sauberem Code, Kontaktformular und SEO-Basis.", "#00b67a", 249),
    ("kevin", "Landingpage fuer dein Produkt", "Schnelle, conversion-starke Landingpage fuer Kampagnen und neue Produkte.", "#169c88", 149),
    ("kevin", "Web-App Fehler beheben", "Analyse und Behebung von Frontend- oder Backend-Problemen in deiner Anwendung.", "#317f72", 89),
    ("demo_design", "Professionelles Logo Design", "Individuelles Logo inklusive Farbwelt und einsatzbereiten Dateiformaten.", "#7457d9", 119),
    ("demo_design", "Komplettes Brand Design", "Markenauftritt mit Logo, Typografie, Farben und kompaktem Styleguide.", "#8c63c7", 299),
    ("demo_design", "Social Media Vorlagen", "Wiederverwendbare Vorlagen fuer Instagram, LinkedIn und weitere Kanaele.", "#a44fa8", 79),
    ("demo_marketing", "Social Media Strategie", "Individuelle Strategie mit Content-Saeulen, Postingplan und Zielgruppenanalyse.", "#e46b3c", 139),
    ("demo_marketing", "SEO Blogartikel schreiben", "Gut recherchierter, suchmaschinenoptimierter Artikel fuer deine Zielgruppe.", "#d8842f", 69),
    ("demo_marketing", "Newsletter Kampagne erstellen", "Konzept, Texte und Betreffzeilen fuer eine komplette E-Mail-Kampagne.", "#c94d45", 99),
    ("demo_video", "Social Media Video schneiden", "Dynamischer Schnitt, Untertitel, Musik und Formatierung fuer deinen Kanal.", "#2878d0", 89),
    ("demo_video", "Produktvideo produzieren", "Hochwertiges Produktvideo aus deinem Material inklusive Motion Graphics.", "#3564bb", 219),
    ("demo_video", "Animiertes Logo erstellen", "Kurze Logoanimation fuer Videos, Praesentationen und Social Media.", "#4b56a5", 109),
]

REVIEWS = [
    ("kevin", "andrey", 5, "Sehr schnelle Umsetzung und eine technisch saubere Website."),
    ("demo_design", "andrey", 5, "Das neue Logo passt perfekt zu unserer Marke."),
    ("demo_marketing", "andrey", 4, "Gute Strategie mit vielen direkt nutzbaren Ideen."),
    ("demo_video", "andrey", 5, "Das Video wirkt professionell und modern."),
    ("kevin", "demo_customer_lena", 5, "Verlaesslich, freundlich und schneller als vereinbart."),
    ("demo_design", "demo_customer_lena", 4, "Sehr schoene Vorlagen und unkomplizierte Abstimmung."),
    ("demo_marketing", "demo_customer_tim", 5, "Der Artikel rankt bereits fuer mehrere relevante Suchbegriffe."),
    ("demo_video", "demo_customer_tim", 4, "Starker Schnitt und gute Auswahl der Musik."),
]


class Command(BaseCommand):
    help = "Create or update realistic demo users, offers, reviews, and orders"

    @transaction.atomic
    def handle(self, *args, **options):
        users = self._seed_users()
        offers = self._seed_offers(users)
        self._seed_reviews(users)
        self._seed_orders(users, offers)
        self.stdout.write(self.style.SUCCESS(
            "Demo data ready: 7 users, 12 offers, 36 packages, "
            "8 reviews, and 6 orders."
        ))

    def _seed_users(self):
        users = {}
        for row in BUSINESSES:
            data = self._business_data(row)
            users[data["username"]] = self._upsert_user(
                data, Profile.UserType.BUSINESS
            )
        for row in CUSTOMERS:
            data = self._customer_data(row)
            users[data["username"]] = self._upsert_user(
                data, Profile.UserType.CUSTOMER
            )
        return users

    def _business_data(self, row):
        keys = [
            "username", "password", "first_name", "last_name", "email",
            "location", "tel", "description", "working_hours", "color",
        ]
        return dict(zip(keys, row))

    def _customer_data(self, row):
        keys = [
            "username", "password", "first_name", "last_name", "email",
            "location", "description", "color",
        ]
        return dict(zip(keys, row))

    def _upsert_user(self, data, user_type):
        User = get_user_model()
        user, created = User.objects.get_or_create(username=data["username"])
        user.email = data["email"]
        if created or not user.check_password(data["password"]):
            user.set_password(data["password"])
        user.save()
        profile, _ = Profile.objects.update_or_create(
            user=user,
            defaults={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "location": data["location"],
                "tel": data.get("tel", ""),
                "description": data["description"],
                "working_hours": data.get("working_hours", ""),
                "type": user_type,
            },
        )
        if not profile.file:
            profile.file.save(
                f"demo-avatar-{data['username']}.jpg",
                self._make_image(
                    data["color"],
                    f"{data['first_name'][0]}{data['last_name'][0]}",
                    (500, 500),
                ),
                save=True,
            )
        return user

    def _seed_offers(self, users):
        seeded = {}
        for username, title, description, color, base_price in OFFERS:
            offer, _ = Offer.objects.update_or_create(
                user=users[username],
                title=title,
                defaults={"description": description},
            )
            if not offer.image:
                offer.image.save(
                    f"demo-{username}-{offer.pk}.jpg",
                    self._make_image(color, title, (1200, 700)),
                    save=True,
                )
            self._seed_offer_details(offer, base_price)
            seeded[(username, title)] = offer
        return seeded

    def _seed_offer_details(self, offer, base_price):
        packages = [
            ("basic", "Basic Paket", base_price, 5, 1, ["Konzept", "Basis-Umsetzung"]),
            ("standard", "Standard Paket", base_price * 2, 3, 3, ["Konzept", "Erweiterte Umsetzung", "Quelldateien"]),
            ("premium", "Premium Paket", base_price * 3, 2, -1, ["Strategie", "Premium-Umsetzung", "Quelldateien", "Priorisierter Support"]),
        ]
        for offer_type, title, price, days, revisions, features in packages:
            OfferDetail.objects.update_or_create(
                offer=offer,
                offer_type=offer_type,
                defaults={
                    "title": title,
                    "price": Decimal(price),
                    "delivery_time_in_days": days,
                    "revisions": revisions,
                    "features": features,
                },
            )

    def _seed_reviews(self, users):
        for business, reviewer, rating, description in REVIEWS:
            Review.objects.update_or_create(
                business_user=users[business],
                reviewer=users[reviewer],
                defaults={"rating": rating, "description": description},
            )

    def _seed_orders(self, users, offers):
        specs = [
            ("andrey", "kevin", "Moderne Business-Website entwickeln", "standard", Order.Status.COMPLETED),
            ("andrey", "demo_design", "Professionelles Logo Design", "premium", Order.Status.COMPLETED),
            ("demo_customer_lena", "demo_marketing", "Social Media Strategie", "standard", Order.Status.IN_PROGRESS),
            ("demo_customer_lena", "demo_video", "Social Media Video schneiden", "basic", Order.Status.COMPLETED),
            ("demo_customer_tim", "kevin", "Landingpage fuer dein Produkt", "premium", Order.Status.IN_PROGRESS),
            ("demo_customer_tim", "demo_design", "Social Media Vorlagen", "standard", Order.Status.COMPLETED),
        ]
        for customer, business, title, offer_type, status in specs:
            offer = offers[(business, title)]
            detail = offer.details.get(offer_type=offer_type)
            Order.objects.update_or_create(
                customer_user=users[customer],
                business_user=users[business],
                title=f"{offer.title} - {detail.title}",
                defaults={
                    "revisions": detail.revisions,
                    "delivery_time_in_days": detail.delivery_time_in_days,
                    "price": detail.price,
                    "features": detail.features,
                    "offer_type": detail.offer_type,
                    "status": status,
                },
            )

    def _make_image(self, color, text, size):
        image = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=max(28, size[0] // 22))
        lines = self._wrap_text(draw, text, font, int(size[0] * 0.78))
        spacing = max(12, size[1] // 35)
        boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
        heights = [box[3] - box[1] for box in boxes]
        y = (size[1] - sum(heights) - spacing * (len(lines) - 1)) / 2
        for line, box, height in zip(lines, boxes, heights):
            width = box[2] - box[0]
            draw.text(((size[0] - width) / 2, y), line, fill="white", font=font)
            y += height + spacing
        output = BytesIO()
        image.save(output, format="JPEG", quality=88)
        return ContentFile(output.getvalue())

    def _wrap_text(self, draw, text, font, max_width):
        lines = []
        current = []
        for word in text.split():
            candidate = " ".join([*current, word])
            if current and draw.textlength(candidate, font=font) > max_width:
                lines.append(" ".join(current))
                current = [word]
            else:
                current.append(word)
        if current:
            lines.append(" ".join(current))
        return lines
