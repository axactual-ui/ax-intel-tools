"""Site settings: edit here (env vars of the same name override)."""
CONTACT_EMAIL = "info@axi68.com"
SQUARE_LINK_FEATURED = "https://square.link/u/07m6l9mD"  # Featured Listing $49/mo
SQUARE_LINK_BANNER = "https://square.link/u/EK11QDcY"    # Top Banner Sponsor $199/mo
SQUARE_LINK_EMAIL = "https://square.link/u/41f27mlm"     # Weekly Email Mention $99 one-time
SUBSCRIBE_FORM_ACTION = ""  # newsletter signup endpoint; empty = email signup via CONTACT_EMAIL
SUB_MONTHLY_URL = "https://square.link/u/WIqYf0JK"  # Early Bird monthly $12.50/mo

# Visitor analytics: Vercel Web Analytics (free Hobby, 50k events/mo). View at vercel.com → project → Analytics.
# No site code needed; script is injected by build.py.

# Sponsor top banner. Flip SPONSOR_BANNER["enabled"] to True after payment + James's go,
# then rebuild (python3 build.py) and deploy. Only one sponsor at a time.
SPONSOR_BANNER = {
    "enabled": True,
    "image": "webz-banner-1200x320.png",
    "href": "https://webz.io/?utm_source=axi68.com&utm_medium=mailing_list&utm_campaign=axi68.com&utm_id=axi68",
    "alt": "Webz.io: Dark web Monitoring APIs",
}
