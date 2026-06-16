AD_AGENCIES = [
    {
        "id": 1,
        "name": "MediaPro Advertising",
        "location": "Chennai, Tamil Nadu",
        "specialization": ["Print Ads", "Digital", "Full Page"],
        "newspapers": ["The Hindu", "Times of India", "Daily Thanthi"],
        "price_range": "₹5,000 — ₹50,000",
        "min_price": 5000,
        "max_price": 50000,
        "rating": 4.8,
        "reviews": 124,
        "contact": "mediaproadv@email.com",
        "phone": "+91 98400 12345",
        "description": "15 years of experience in print and digital advertising across major Indian newspapers.",
        "turnaround": "3-5 days"
    },
    {
        "id": 2,
        "name": "AdVantage Solutions",
        "location": "Mumbai, Maharashtra",
        "specialization": ["Half Page", "Quarter Page", "Classifieds"],
        "newspapers": ["Times of India", "Indian Express", "NDTV"],
        "price_range": "₹8,000 — ₹75,000",
        "min_price": 8000,
        "max_price": 75000,
        "rating": 4.6,
        "reviews": 89,
        "contact": "info@advantagesol.com",
        "phone": "+91 98200 54321",
        "description": "Specializing in metro newspaper advertising with guaranteed placement.",
        "turnaround": "2-4 days"
    },
    {
        "id": 3,
        "name": "Tamil Nadu Ad Bureau",
        "location": "Chennai, Tamil Nadu",
        "specialization": ["Tamil Newspapers", "Regional Ads", "Classifieds"],
        "newspapers": ["Daily Thanthi", "Dinamalar", "Dinakaran"],
        "price_range": "₹2,000 — ₹25,000",
        "min_price": 2000,
        "max_price": 25000,
        "rating": 4.9,
        "reviews": 203,
        "contact": "tnadbureau@email.com",
        "phone": "+91 94440 67890",
        "description": "Leading regional advertising agency specializing in Tamil language newspapers.",
        "turnaround": "1-3 days"
    },
    {
        "id": 4,
        "name": "National Press Ads",
        "location": "New Delhi",
        "specialization": ["Front Page", "Full Page", "Color Ads"],
        "newspapers": ["The Hindu", "Times of India", "Indian Express", "NDTV"],
        "price_range": "₹15,000 — ₹2,00,000",
        "min_price": 15000,
        "max_price": 200000,
        "rating": 4.7,
        "reviews": 156,
        "contact": "contact@nationalpressads.com",
        "phone": "+91 98110 11223",
        "description": "Premium advertising solutions for national newspaper placements across India.",
        "turnaround": "5-7 days"
    },
    {
        "id": 5,
        "name": "QuickAd Services",
        "location": "Bangalore, Karnataka",
        "specialization": ["Classifieds", "Obituary", "Public Notice"],
        "newspapers": ["The Hindu", "Times of India", "Deccan Herald"],
        "price_range": "₹500 — ₹10,000",
        "min_price": 500,
        "max_price": 10000,
        "rating": 4.5,
        "reviews": 312,
        "contact": "quickad@email.com",
        "phone": "+91 98860 44556",
        "description": "Fast and affordable classified and public notice advertising.",
        "turnaround": "Same day — 2 days"
    },
    {
        "id": 6,
        "name": "BrandFirst Media",
        "location": "Hyderabad, Telangana",
        "specialization": ["Brand Campaigns", "Full Page", "Color Ads"],
        "newspapers": ["The Hindu", "Times of India", "Deccan Chronicle"],
        "price_range": "₹20,000 — ₹1,50,000",
        "min_price": 20000,
        "max_price": 150000,
        "rating": 4.4,
        "reviews": 67,
        "contact": "hello@brandfirstmedia.com",
        "phone": "+91 98490 77889",
        "description": "Creative brand campaigns with strategic newspaper placement.",
        "turnaround": "4-6 days"
    },
    {
        "id": 7,
        "name": "SmallBiz Ads",
        "location": "Chennai, Tamil Nadu",
        "specialization": ["Small Business", "Classifieds", "Local Ads"],
        "newspapers": ["Daily Thanthi", "The Hindu", "Times of India"],
        "price_range": "₹500 — ₹8,000",
        "min_price": 500,
        "max_price": 8000,
        "rating": 4.3,
        "reviews": 445,
        "contact": "smallbizads@email.com",
        "phone": "+91 97890 33445",
        "description": "Affordable advertising solutions designed specifically for small businesses.",
        "turnaround": "1-2 days"
    },
    {
        "id": 8,
        "name": "Corporate Press India",
        "location": "Mumbai, Maharashtra",
        "specialization": ["Corporate Announcements", "IPO Ads", "Legal Notices"],
        "newspapers": ["The Hindu", "Times of India", "Indian Express", "Financial Express"],
        "price_range": "₹25,000 — ₹5,00,000",
        "min_price": 25000,
        "max_price": 500000,
        "rating": 4.9,
        "reviews": 78,
        "contact": "info@corporatepressindia.com",
        "phone": "+91 98200 99001",
        "description": "Specialized in corporate, legal, and financial newspaper advertisements.",
        "turnaround": "2-3 days"
    },
    {
        "id": 9,
        "name": "EventAd Promotions",
        "location": "Pune, Maharashtra",
        "specialization": ["Event Promotions", "Entertainment", "Color Ads"],
        "newspapers": ["Times of India", "Indian Express", "Sakal"],
        "price_range": "₹3,000 — ₹40,000",
        "min_price": 3000,
        "max_price": 40000,
        "rating": 4.6,
        "reviews": 134,
        "contact": "eventad@email.com",
        "phone": "+91 98220 55667",
        "description": "Creative event promotion advertising with eye-catching designs.",
        "turnaround": "2-4 days"
    },
    {
        "id": 10,
        "name": "EduAds Network",
        "location": "Chennai, Tamil Nadu",
        "specialization": ["Education Ads", "Admissions", "Recruitment"],
        "newspapers": ["The Hindu", "Daily Thanthi", "Times of India"],
        "price_range": "₹2,500 — ₹30,000",
        "min_price": 2500,
        "max_price": 30000,
        "rating": 4.7,
        "reviews": 289,
        "contact": "eduads@email.com",
        "phone": "+91 94440 22334",
        "description": "Specialized in educational institution advertising and recruitment campaigns.",
        "turnaround": "1-3 days"
    }
]

def get_all_agencies(newspaper=None, max_budget=None, specialization=None):
    agencies = AD_AGENCIES.copy()

    if newspaper and newspaper != "All":
        agencies = [a for a in agencies if newspaper in a["newspapers"]]

    if max_budget:
        agencies = [a for a in agencies if a["min_price"] <= int(max_budget)]

    if specialization:
        agencies = [a for a in agencies if any(
            specialization.lower() in s.lower() for s in a["specialization"]
        )]

    return sorted(agencies, key=lambda x: x["rating"], reverse=True)

def get_agency_by_id(agency_id):
    for agency in AD_AGENCIES:
        if agency["id"] == agency_id:
            return agency
    return None
    