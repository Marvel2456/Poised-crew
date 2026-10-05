import datetime
from django.core.management.base import BaseCommand
from agency.models import Service, EventPortfolio, UniformStyle, GalleryItem, Testimonial


class Command(BaseCommand):
    help = 'Populates the database with rich seed data for The Poised Crew'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing old seed data..."))
        Service.objects.all().delete()
        EventPortfolio.objects.all().delete()
        UniformStyle.objects.all().delete()
        GalleryItem.objects.all().delete()
        Testimonial.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating Services..."))
        
        services_data = [
            {
                "title": "VIP & Diplomatic Protocol",
                "category": "protocol",
                "badge_text": "VIP Exclusive",
                "icon_name": "crown",
                "short_description": "Elite protocol officers trained in diplomatic etiquette, high-table choreography, and dignitary liaison.",
                "full_description": "Our VIP Protocol service is designed for state banquets, high-level diplomatic assemblies, and executive retreats. Our officers undergo rigorous training in international diplomatic precedence, escort formation, bilateral meeting room management, and security liaison.",
                "deliverables": "Diplomatic Order of Precedence Planning\nRed-Carpet Dignitary Escort & Reception\nHigh-Table & Presidential Lounge Hosting\nState Anthem & Toast Etiquette Coordination\nDedicated Protocol Lead & Radio Communications\nDiscreet Executive Concierge Service",
                "suitable_events": "Government & State Banquets\nAmbassadorial & Diplomatic Summits\nCEO & Board of Directors Retreats\nHigh-Profile Royal Ceremonies",
                "uniform_recommendations": "Imperial Obsidian Black-Tie / Velvet Lapel Suiting with Silk Gold Cravats",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Event Ushering & Guest Reception",
                "category": "ushering",
                "badge_text": "Most Popular",
                "icon_name": "users",
                "short_description": "Warm, immaculate, and highly coordinated ushers providing flawless hospitality from arrival to departure.",
                "full_description": "The hallmark of The Poised Crew. We transform standard ushering into a five-star hospitality experience. From welcoming guests with poise and warmth to orchestrating banquet seating, gift handling, and program distribution, our crew ensures every attendee feels like royalty.",
                "deliverables": "Warm Guest Greeting & Directional Guidance\nBanquet Table Seating Choreography\nMenu & Program Order Distribution\nGift & Souvenir Registry Management\nHostess Support for Celebrants\nCleanliness & Hall Ambiance Monitoring",
                "suitable_events": "Luxury Weddings & Traditional Engagements\nMilestone Birthday Galas & Anniversaries\nCorporate Dinners & Soirées\nCharity & Foundation Balls",
                "uniform_recommendations": "Classic Gold & Black Luxury Gowns or Tailored Tuxedos",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Registration & Digital Check-In",
                "category": "corporate",
                "badge_text": "Tech-Enabled",
                "icon_name": "qr-code",
                "short_description": "Rapid digital badge printing, QR code scanning, delegate accreditation, and welcome pack distribution.",
                "full_description": "Eliminate entrance queues with our tech-savvy registration teams. Equipped to handle digital check-in platforms, QR accreditation scanners, badge printers, and VIP delegate tracking with speed and immaculate courtesy.",
                "deliverables": "QR Code Scanning & Instant Badge Issuance\nVIP vs Delegate Stream Management\nWelcome Kits & Swag Bag Distribution\nOn-Site Real-Time Attendance Reporting\nSpeaker & Press Accreditation Handling\nHelpdesk & Info Point Support",
                "suitable_events": "International Conferences & Tech Summits\nAnnual General Meetings (AGMs)\nTrade Expos & Industry Conventions\nExecutive Masterclasses",
                "uniform_recommendations": "Contemporary Corporate Suiting with Gold Identifier Badges",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "Red-Carpet & Media Wall Management",
                "category": "protocol",
                "badge_text": "High Visibility",
                "icon_name": "camera",
                "short_description": "Choreographed guest pacing, backdrop photo coordination, and media interview staging.",
                "full_description": "Ensure your red carpet runs with elegance and order. Our trained hostesses manage media lines, ensure sponsors' logos are never obscured on the media wall, guide celebrities and VIPs through press interviews, and keep arrivals moving smoothly.",
                "deliverables": "Arrival Pacing & Red-Carpet Flow Control\nMedia Wall / Step-and-Repeat Coordination\nCelebrity & VIP Press Line Escort\nVIP Gift Bag Handover at Carpet Exit\nCoordination with Paparazzi & Broadcast Crews",
                "suitable_events": "Award Ceremonies & Gala Nights\nMovie Premieres & Film Festivals\nFashion Week & Runway Shows\nHigh-End Brand Launches",
                "uniform_recommendations": "Sleek Haute Couture Evening Gowns / Black Tuxedo with Gold Accents",
                "is_featured": True,
                "order": 4,
            },
            {
                "title": "Conference & Summit Coordination",
                "category": "corporate",
                "badge_text": "Corporate Tier",
                "icon_name": "briefcase",
                "short_description": "Breakout hall coordination, microphone runners, speaker timekeeping, and stage logistics.",
                "full_description": "Seamless execution for multi-hall business congresses. Our corporate crew manages auditorium seating, roving microphones for audience Q&A, speaker stage escort, timekeeping cue cards, and VIP green room hospitality.",
                "deliverables": "Roving Microphone Runners with Padded Covers\nPlenary & Breakout Hall Access Management\nSpeaker Stage Arrival & Podium Assistance\nSession Timekeeping & Audience Seating\nVIP Green Room Concierge",
                "suitable_events": "Banking & Energy Summits\nPan-African Policy Forums\nGlobal Investor Conferences\nAcademic & Healthcare Congresses",
                "uniform_recommendations": "Executive Midnight Navy & Gold Suiting with Silk Cravats",
                "is_featured": False,
                "order": 5,
            },
            {
                "title": "Luxury Weddings & Traditional Galas",
                "category": "ushering",
                "badge_text": "Signature Craft",
                "icon_name": "heart",
                "short_description": "Regal hospitality aligned with cultural etiquette, bridal assistance, and family VIP care.",
                "full_description": "From royal Nigerian traditional weddings (Yoruba, Igbo, Edo, Hausa/Fulani, Niger-Delta) to contemporary white wedding receptions. We ensure the bridal party, royal fathers, and distinguished guests enjoy effortless luxury.",
                "deliverables": "Bridal Train & Groom's Entourage Liaison\nFamily VIP & Royal Elders Seating Protocol\nSpraying / Currency Collection Security Liaison\nSouvenir & Champagne Service Supervision\nFloor Coordination with Caterers & Decorators",
                "suitable_events": "Luxury Destination Weddings\nTraditional Engagements & Coronations\nHigh-Society Reception Dinners\nBridal Showcases & Anniversaries",
                "uniform_recommendations": "Royal Velvet Aso-Ebi Aligned or Imperial Black-Tie",
                "is_featured": True,
                "order": 6,
            },
            {
                "title": "Airport VIP Reception & Chaperone",
                "category": "specialist",
                "badge_text": "Concierge",
                "icon_name": "plane",
                "short_description": "Tarmac and arrivals hall protocol, fast-track immigration liaison, and luxury convoy chaperone.",
                "full_description": "Make an unforgettable first impression the moment your international dignitaries land. Our protocol officers manage tarmac greetings, lounge hospitality, baggage handling coordination, and escort to awaiting motorcades.",
                "deliverables": "Meet & Greet at VIP / Presidential Lounge\nFast-Track Customs & Immigration Liaison\nLuggage Tagging & Porterage Oversight\nChauffeur / Motorcade Dispatch Coordination\nHotel Check-In Pre-Arrival Verification",
                "suitable_events": "International Summits & Head of State Visits\nCelebrity & Keynote Speaker Arrivals\nLuxury Destination Wedding Guests\nMultinational Executive Delegations",
                "uniform_recommendations": "Crisp Airport Protocol Blazer & Gold Epaulettes",
                "is_featured": False,
                "order": 7,
            },
            {
                "title": "Award Ceremonies & Stage Management",
                "category": "specialist",
                "badge_text": "Live Broadcast",
                "icon_name": "award",
                "short_description": "Plaque/trophy presentation on stage, winner escort, envelope handoff, and broadcast cueing.",
                "full_description": "Flawless timing for televised and live award nights. Our stage hostesses present trophies with immaculate posture, guide winners to podiums, and manage envelope handoffs in sync with stage directors.",
                "deliverables": "Trophy & Certificate Stage Presentation\nWinner Escort from Seating to Stage & Media Room\nSealed Envelope Handover to Presenters\nMicrophone & Podium Height Adjustment Assistance\nLive TV Broadcast Cue Synchronization",
                "suitable_events": "Music & Film Awards\nIndustry Excellence Galas\nCorporate Recognition Banquets\nSports Honors & Hall of Fame Dinners",
                "uniform_recommendations": "Grand Gala Floor-Length Gold Shimmer Dresses / Black Tuxedos",
                "is_featured": False,
                "order": 8,
            },
            {
                "title": "Crowd & Guest Flow Management",
                "category": "specialist",
                "badge_text": "Logistics",
                "icon_name": "shield-check",
                "short_description": "Hall entrance regulation, overflow area guidance, rapid seating transitions, and security liaison.",
                "full_description": "For large-scale gatherings of 1,000+ guests. Our team maintains serene order, prevents bottlenecks at entry gates, manages overflow zones, and liaises directly with private security and medical personnel.",
                "deliverables": "Entry Gate Flow & Queue Line Choreography\nVIP vs General Admission Demarcation\nOverflow Hall Transitions & Seating Guidance\nEmergency Exit Route Monitoring\nDirect Radio Link with Private Security Detail",
                "suitable_events": "Stadium Concerts & Megachurch Conventions\nProduct Expos & Trade Fairs\nPolitical Rallies & National Congresses",
                "uniform_recommendations": "High-Visibility Gold Armband Protocol Attire",
                "is_featured": False,
                "order": 9,
            }
        ]

        for s_data in services_data:
            Service.objects.create(**s_data)

        self.stdout.write(self.style.SUCCESS("Creating Event Portfolio Case Studies..."))
        
        portfolio_data = [
            {
                "title": "West Africa Tech Leadership Summit 2026",
                "category": "conference",
                "date_held": datetime.date(2026, 4, 18),
                "location": "Eko Convention Centre, Victoria Island",
                "city": "Lagos, Nigeria",
                "client_name": "AfriTech Innovations & Venture Capital",
                "planner_name": "Zenith Horizon Events",
                "crew_deployed": 36,
                "services_provided": "VIP Protocol • Digital QR Check-In • 4 Breakout Halls • Stage Coordination",
                "summary": "The premier technology summit in West Africa welcoming 2,800 delegates, 40 international venture funds, and ministers of technology from 6 African nations. The Poised Crew managed the entire delegate journey from airport arrival to registration and VIP high-table protocol.",
                "highlight_result": "2,800+ Delegates accredited in under 40 minutes with zero entry bottleneck.",
                "image_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "The Royal Ebony Wedding Gala",
                "category": "wedding",
                "date_held": datetime.date(2026, 2, 14),
                "location": "Balmoral Hall, Federal Palace Hotel",
                "city": "Lagos, Nigeria",
                "client_name": "Dr. & Mrs. Adeleke-Cole",
                "planner_name": "Zapphaire Events Luxury",
                "crew_deployed": 28,
                "services_provided": "Guest Reception • Royal Seating Protocol • Bridal Train Liaison • Souvenir Control",
                "summary": "A grand high-society celebration with 850 distinguished guests including state governors, royal fathers, and captains of industry. The crew donned customized emerald and royal gold velvet attire aligned with the couple's royal theme.",
                "highlight_result": "Seamless seating of 850 guests across 85 banquet tables with 100% precision.",
                "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Federal Diplomatic & Trade Banquet",
                "category": "government",
                "date_held": datetime.date(2026, 5, 2),
                "location": "Transcorp Hilton Congress Hall",
                "city": "Abuja, FCT",
                "client_name": "Federal Ministry of Foreign Affairs & Trade",
                "planner_name": "Diplomatic Protocol Directorate",
                "crew_deployed": 42,
                "services_provided": "Ambassadorial Protocol • High Table Escort • National Anthem Etiquette",
                "summary": "Hosting 32 foreign ambassadors, trade commissioners, and executive ministers. The Poised Crew's multilingual protocol officers conducted ceremonial entrance escorts and high-table dining choreography according to strict state order of precedence.",
                "highlight_result": "Commended by the Chief of Protocol for impeccable diplomatic etiquette.",
                "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "Pan-African Music & Creative Honors 2026",
                "category": "entertainment",
                "date_held": datetime.date(2026, 3, 28),
                "location": "Landmark Event Centre, Oniru",
                "city": "Lagos, Nigeria",
                "client_name": "SoundCity & Pan-African Creative Council",
                "planner_name": "Red Carpet Masters Media",
                "crew_deployed": 30,
                "services_provided": "Red Carpet Pacing • Media Wall Flow • Stage Trophy Presentation • VIP Lounge",
                "summary": "Live broadcasted to over 15 million viewers across Africa. The Poised Crew managed red carpet arrivals for 120+ celebrities and executed 24 on-stage award handoffs with synchronized broadcast timing.",
                "highlight_result": "100% on-time stage handovers with flawless TV camera sightlines.",
                "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80",
                "is_featured": True,
                "order": 4,
            },
            {
                "title": "Zenith Global Banking & Wealth Forum",
                "category": "corporate",
                "date_held": datetime.date(2026, 6, 10),
                "location": "Civic Centre, Victoria Island",
                "city": "Lagos, Nigeria",
                "client_name": "Zenith & Apex Wealth Advisory",
                "planner_name": "Elite Corporate Planners",
                "crew_deployed": 24,
                "services_provided": "Executive Accreditation • Breakout Room Logistics • Speaker Timekeeping",
                "summary": "An exclusive private wealth gathering for ultra-high-net-worth investors and fund managers. Our corporate protocol officers ensured strict confidentiality and pristine hospitality.",
                "highlight_result": "Zero confidentiality breaches and 5-star feedback from board directors.",
                "image_url": "https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&w=1200&q=80",
                "is_featured": False,
                "order": 5,
            },
            {
                "title": "Lagos International Luxury Real Estate Expo",
                "category": "exhibition",
                "date_held": datetime.date(2026, 7, 5),
                "location": "The Federal Palace Oceanview Marquee",
                "city": "Lagos, Nigeria",
                "client_name": "West Africa Property Developers Association",
                "planner_name": "Global Expos Africa",
                "crew_deployed": 32,
                "services_provided": "Exhibition Booth Hostesses • VIP Buyer Escort • Investor Lounge Concierge",
                "summary": "A 3-day exhibition featuring luxury real estate across Dubai, London, Lagos, and Kigali. The Poised Crew provided multilingual booth hostesses who handled investor lead acquisition and VIP buyers.",
                "highlight_result": "Managed over 4,500 visiting property investors across 3 days.",
                "image_url": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=1200&q=80",
                "is_featured": False,
                "order": 6,
            }
        ]

        for p_data in portfolio_data:
            EventPortfolio.objects.create(**p_data)

        self.stdout.write(self.style.SUCCESS("Creating Uniform Styles..."))
        
        uniforms = [
            {
                "name": "Imperial Black-Tie Tuxedo & Evening Gowns",
                "tag": "VIP Galas & Red Carpets",
                "description": "Tailored double-breasted obsidian black tuxedos with satin peak lapels for male officers, and floor-length bespoke black gowns with gold brocade trims for female officers.",
                "gender": "Male & Female Matching",
                "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
                "color_palette": "Obsidian Black, Satin Trim, Gold Pocket Square",
            },
            {
                "name": "Royal Velvet & Brocade (Aso-Ebi Aligned)",
                "tag": "Luxury Weddings & Coronations",
                "description": "Rich emerald or burgundy velvet tailored blazers paired with champagne gold accents, customized to match the celebrant's royal colour code.",
                "gender": "Unisex / Male & Female",
                "image_url": "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?auto=format&fit=crop&w=800&q=80",
                "color_palette": "Royal Emerald / Burgundy & Champagne Gold",
            },
            {
                "name": "Corporate Obsidian & Gold Suiting",
                "tag": "Summits, AGMs & Conferences",
                "description": "Contemporary structured blazer sets with bespoke silk gold cravats/scarves and engraved gold nameplates for executive corporate decorum.",
                "gender": "Male & Female Sets",
                "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80",
                "color_palette": "Deep Midnight Charcoal & Imperial Gold Silk",
            },
            {
                "name": "Monochrome Minimalist Hostess Wear",
                "tag": "Product Launches & Brand Activations",
                "description": "Clean-cut, elegant midi dresses or chic jumpsuits featuring sleek metallic belts, designed for vibrant brand visibility and effortless agility.",
                "gender": "Female Hostess Ensemble",
                "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
                "color_palette": "Matte Obsidian Black & Gold Accents",
            },
        ]

        for u in uniforms:
            UniformStyle.objects.create(**u)

        self.stdout.write(self.style.SUCCESS("Creating Gallery Items..."))
        
        gallery = [
            {"title": "VIP High Table Protocol", "category": "protocol", "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80", "caption": "Officers coordinating dignitary seating at Federal Summit", "order": 1},
            {"title": "Tech Summit Registration Desk", "category": "conferences", "image_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80", "caption": "Accreditation and badge scanning for 2,800 delegates", "order": 2},
            {"title": "Red Carpet Media Wall Pacing", "category": "events", "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=800&q=80", "caption": "Celebrity arrivals at the Pan-African Music Awards", "order": 3},
            {"title": "Royal Wedding Reception Ushers", "category": "weddings", "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80", "caption": "Immaculate bridal party escort and VIP table service", "order": 4},
            {"title": "Pre-Event Briefing & Alignment", "category": "bts", "image_url": "https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=800&q=80", "caption": "Lead supervisor conducting 60-minute pre-call inspection", "order": 5},
            {"title": "Imperial Black-Tie Uniform Showcase", "category": "uniforms", "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80", "caption": "Standard Black-Tie attire with gold pocket square & pins", "order": 6},
            {"title": "Stage Presentation at Honors Gala", "category": "events", "image_url": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80", "caption": "Plaque and trophy handovers on live television", "order": 7},
            {"title": "Diplomatic Airport Escort", "category": "protocol", "image_url": "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?auto=format&fit=crop&w=800&q=80", "caption": "VIP tarmac reception for visiting foreign delegation", "order": 8},
        ]

        for g in gallery:
            GalleryItem.objects.create(**g)

        self.stdout.write(self.style.SUCCESS("Creating Testimonials..."))
        
        testimonials = [
            {
                "client_name": "Oluwaseun Adeyemi",
                "client_role_company": "Chief Operating Officer, Zenith Horizon Events",
                "event_name": "West Africa Tech Leadership Summit",
                "quote": "The Poised Crew set a new benchmark for corporate ushering in Nigeria. Their protocol officers handled 2,800 international delegates with immaculate precision, zero queue panic, and infectious warmth. They are our permanent event partner.",
                "rating": 5,
                "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
                "is_featured": True,
            },
            {
                "client_name": "Folashade Balogun",
                "client_role_company": "Lead Wedding Planner, Zapphaire Luxury Weddings",
                "event_name": "The Royal Ebony Wedding Gala",
                "quote": "When managing weddings with 4 state governors and monarchs present, you cannot afford amateur ushers. The Poised Crew understood every nuance of Yoruba and diplomatic protocol. Their posture, poise, and punctuality were flawless.",
                "rating": 5,
                "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
                "is_featured": True,
            },
            {
                "client_name": "Ambassador Ibrahim Mukhtar",
                "client_role_company": "Special Envoy, African Trade Directorate",
                "event_name": "Federal Diplomatic & Trade Banquet",
                "quote": "Their officers' grasp of diplomatic seating precedence and discreet high-table hospitality rivaled state protocol services in Geneva and London. Truly living up to their name — pure poise.",
                "rating": 5,
                "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
                "is_featured": True,
            }
        ]

        for t in testimonials:
            Testimonial.objects.create(**t)

        self.stdout.write(self.style.SUCCESS("Successfully seeded The Poised Crew database!"))
