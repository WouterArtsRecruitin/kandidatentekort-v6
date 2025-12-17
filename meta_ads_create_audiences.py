#!/usr/bin/env python3
"""
Meta Ads Custom Audiences Creator voor Kandidatentekort.nl
==========================================================

Dit script maakt alle benodigde Custom Audiences aan voor de funnel:
- Website visitors (verschillende retentieperiodes)
- Video viewers (25%, 50%, 75%, 95%)
- Page/Post engagers
- Form starters (event-based)
- Lookalike audiences

VEREISTEN:
1. Facebook Marketing API access token
2. Ad Account ID
3. Pixel ID (voor website audiences)
4. Page ID (voor engagement audiences)
5. pip install facebook-business

GEBRUIK:
    python meta_ads_create_audiences.py --token YOUR_TOKEN --account act_123 --pixel 123 --page 456

OF met environment variables:
    export META_ACCESS_TOKEN=your_token
    export META_AD_ACCOUNT=act_1236576254450117
    export META_PIXEL_ID=your_pixel_id
    export META_PAGE_ID=your_page_id
    python meta_ads_create_audiences.py
"""

import os
import sys
import json
import argparse
from datetime import datetime

try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.customaudience import CustomAudience
    from facebook_business.adobjects.page import Page
except ImportError:
    print("❌ facebook-business package niet gevonden.")
    print("   Installeer met: pip install facebook-business")
    sys.exit(1)


# =============================================================================
# AUDIENCE CONFIGURATION
# =============================================================================

# Website Custom Audiences (Pixel-based)
WEBSITE_AUDIENCES = [
    {
        "name": "KT - All Website Visitors 180d",
        "description": "Alle bezoekers kandidatentekort.nl - laatste 180 dagen",
        "retention_days": 180,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 15552000,  # 180 days
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": "kandidatentekort.nl"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "TOFU",
    },
    {
        "name": "KT - Website Visitors 30d",
        "description": "Bezoekers kandidatentekort.nl - laatste 30 dagen",
        "retention_days": 30,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 2592000,  # 30 days
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": "kandidatentekort.nl"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "MOFU",
    },
    {
        "name": "KT - Website Visitors 14d",
        "description": "Bezoekers kandidatentekort.nl - laatste 14 dagen (hot retarget)",
        "retention_days": 14,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 1209600,  # 14 days
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": "kandidatentekort.nl"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "BOFU",
    },
    {
        "name": "KT - Website Visitors 7d",
        "description": "Bezoekers kandidatentekort.nl - laatste 7 dagen (hottest)",
        "retention_days": 7,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 604800,  # 7 days
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": "kandidatentekort.nl"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "BOFU",
    },
]

# Event-based Website Audiences
EVENT_AUDIENCES = [
    {
        "name": "KT - Form Starters",
        "description": "Bezoekers die form zijn gestart maar niet afgerond",
        "retention_days": 30,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 2592000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "InitiateCheckout"  # of custom event
                                }
                            ]
                        }
                    }
                ]
            },
            "exclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 2592000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "Lead"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "BOFU",
    },
    {
        "name": "KT - Converters (Leads)",
        "description": "Bezoekers die form hebben ingevuld - voor exclusion",
        "retention_days": 180,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [{"type": "pixel", "id": "PIXEL_ID"}],
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "Lead"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "CONVERTED",
        "use_for": "exclusion",
    },
]

# Video Engagement Audiences
VIDEO_AUDIENCES = [
    {
        "name": "KT - Video Viewers 25%",
        "description": "Mensen die 25% van KT video's hebben bekeken",
        "retention_days": 365,
        "subtype": "ENGAGEMENT",
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 31536000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "video_watched"
                                },
                                {
                                    "field": "video_watched.video_view_percent_threshold",
                                    "operator": "eq",
                                    "value": "25"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "TOFU",
    },
    {
        "name": "KT - Video Viewers 50%",
        "description": "Mensen die 50% van KT video's hebben bekeken",
        "retention_days": 365,
        "subtype": "ENGAGEMENT",
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 31536000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "video_watched"
                                },
                                {
                                    "field": "video_watched.video_view_percent_threshold",
                                    "operator": "eq",
                                    "value": "50"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "MOFU",
    },
    {
        "name": "KT - Video Viewers 75%",
        "description": "Mensen die 75% van KT video's hebben bekeken",
        "retention_days": 365,
        "subtype": "ENGAGEMENT",
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 31536000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "video_watched"
                                },
                                {
                                    "field": "video_watched.video_view_percent_threshold",
                                    "operator": "eq",
                                    "value": "75"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "MOFU",
    },
    {
        "name": "KT - Video Viewers 95%",
        "description": "Mensen die 95% van KT video's hebben bekeken (high intent)",
        "retention_days": 365,
        "subtype": "ENGAGEMENT",
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 31536000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": "video_watched"
                                },
                                {
                                    "field": "video_watched.video_view_percent_threshold",
                                    "operator": "eq",
                                    "value": "95"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "funnel_stage": "BOFU",
    },
]

# Page/Post Engagement Audiences
ENGAGEMENT_AUDIENCES = [
    {
        "name": "KT - Page Engagers 30d",
        "description": "Mensen die engaged hebben met FB/IG page laatste 30 dagen",
        "retention_days": 30,
        "subtype": "ENGAGEMENT",
        "prefill": True,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 2592000,
                    }
                ]
            }
        },
        "funnel_stage": "MOFU",
    },
    {
        "name": "KT - Page Engagers 60d",
        "description": "Mensen die engaged hebben met FB/IG page laatste 60 dagen",
        "retention_days": 60,
        "subtype": "ENGAGEMENT",
        "prefill": True,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 5184000,
                    }
                ]
            }
        },
        "funnel_stage": "TOFU",
    },
    {
        "name": "KT - Page Engagers 90d",
        "description": "Mensen die engaged hebben met FB/IG page laatste 90 dagen",
        "retention_days": 90,
        "subtype": "ENGAGEMENT",
        "prefill": True,
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "object_id": "PAGE_ID",
                        "event_sources": [{"type": "page", "id": "PAGE_ID"}],
                        "retention_seconds": 7776000,
                    }
                ]
            }
        },
        "funnel_stage": "TOFU",
    },
]

# Lookalike Audiences (created from source audiences)
LOOKALIKE_CONFIGS = [
    {
        "name": "KT - LAL 1% Website Visitors",
        "description": "1% Lookalike van website bezoekers",
        "source_audience": "KT - All Website Visitors 180d",
        "country": "NL",
        "ratio": 0.01,  # 1%
    },
    {
        "name": "KT - LAL 2% Website Visitors",
        "description": "2% Lookalike van website bezoekers",
        "source_audience": "KT - All Website Visitors 180d",
        "country": "NL",
        "ratio": 0.02,  # 2%
    },
    {
        "name": "KT - LAL 1% Converters",
        "description": "1% Lookalike van converters (beste audience)",
        "source_audience": "KT - Converters (Leads)",
        "country": "NL",
        "ratio": 0.01,
    },
    {
        "name": "KT - LAL 1% Video 75%",
        "description": "1% Lookalike van 75% video viewers",
        "source_audience": "KT - Video Viewers 75%",
        "country": "NL",
        "ratio": 0.01,
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def log(message: str, level: str = "INFO"):
    """Print log message met timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "ACTION": "🔧",
        "CREATE": "➕",
        "SKIP": "⏭️",
    }
    icon = icons.get(level, "•")
    print(f"[{timestamp}] {icon} {message}")


def replace_ids_in_rule(rule: dict, pixel_id: str, page_id: str) -> dict:
    """Vervang placeholder IDs in rule definitie"""
    rule_str = json.dumps(rule)
    rule_str = rule_str.replace('"PIXEL_ID"', f'"{pixel_id}"')
    rule_str = rule_str.replace('"PAGE_ID"', f'"{page_id}"')
    return json.loads(rule_str)


# =============================================================================
# API FUNCTIONS
# =============================================================================

def initialize_api(access_token: str, ad_account_id: str) -> AdAccount:
    """Initialize Facebook Marketing API"""
    log(f"Initialiseren API voor account: {ad_account_id}")
    FacebookAdsApi.init(access_token=access_token)
    return AdAccount(ad_account_id)


def get_existing_audiences(account: AdAccount) -> dict:
    """Haal bestaande audiences op en return als dict {name: id}"""
    log("Ophalen bestaande audiences...")
    
    fields = [
        CustomAudience.Field.id,
        CustomAudience.Field.name,
        CustomAudience.Field.subtype,
        CustomAudience.Field.approximate_count,
    ]
    
    audiences = account.get_custom_audiences(fields=fields)
    
    audience_map = {}
    for aud in audiences:
        audience_map[aud[CustomAudience.Field.name]] = {
            "id": aud[CustomAudience.Field.id],
            "subtype": aud.get(CustomAudience.Field.subtype),
            "size": aud.get(CustomAudience.Field.approximate_count, 0),
        }
    
    log(f"Gevonden: {len(audience_map)} bestaande audiences")
    return audience_map


def create_website_audience(
    account: AdAccount,
    config: dict,
    pixel_id: str,
    existing: dict,
    dry_run: bool = True
) -> CustomAudience:
    """Maak website custom audience aan"""
    name = config["name"]
    
    # Check if exists
    if name in existing:
        log(f"Audience bestaat al: {name} (ID: {existing[name]['id']})", "SKIP")
        return None
    
    log(f"Aanmaken: {name}", "CREATE")
    
    # Replace pixel ID in rule
    rule = replace_ids_in_rule(config["rule"], pixel_id, "")
    
    params = {
        CustomAudience.Field.name: name,
        CustomAudience.Field.description: config.get("description", ""),
        CustomAudience.Field.subtype: "WEBSITE",
        CustomAudience.Field.retention_days: config["retention_days"],
        CustomAudience.Field.rule: json.dumps(rule),
        CustomAudience.Field.prefill: True,
        CustomAudience.Field.customer_file_source: "USER_PROVIDED_ONLY",
    }
    
    if dry_run:
        log(f"[DRY RUN] Zou aanmaken: {name}")
        log(f"          Retention: {config['retention_days']} dagen")
        log(f"          Funnel: {config.get('funnel_stage', 'N/A')}")
        return None
    
    try:
        audience = account.create_custom_audience(params=params)
        log(f"Aangemaakt: {name} (ID: {audience['id']})", "SUCCESS")
        return audience
    except Exception as e:
        log(f"Fout bij aanmaken {name}: {e}", "ERROR")
        return None


def create_engagement_audience(
    account: AdAccount,
    config: dict,
    page_id: str,
    existing: dict,
    dry_run: bool = True
) -> CustomAudience:
    """Maak engagement custom audience aan"""
    name = config["name"]
    
    if name in existing:
        log(f"Audience bestaat al: {name} (ID: {existing[name]['id']})", "SKIP")
        return None
    
    log(f"Aanmaken: {name}", "CREATE")
    
    # Replace page ID in rule
    rule = replace_ids_in_rule(config["rule"], "", page_id)
    
    params = {
        CustomAudience.Field.name: name,
        CustomAudience.Field.description: config.get("description", ""),
        CustomAudience.Field.subtype: config.get("subtype", "ENGAGEMENT"),
        CustomAudience.Field.rule: json.dumps(rule),
        CustomAudience.Field.prefill: config.get("prefill", True),
    }
    
    if dry_run:
        log(f"[DRY RUN] Zou aanmaken: {name}")
        log(f"          Type: {config.get('subtype', 'ENGAGEMENT')}")
        log(f"          Funnel: {config.get('funnel_stage', 'N/A')}")
        return None
    
    try:
        audience = account.create_custom_audience(params=params)
        log(f"Aangemaakt: {name} (ID: {audience['id']})", "SUCCESS")
        return audience
    except Exception as e:
        log(f"Fout bij aanmaken {name}: {e}", "ERROR")
        return None


def create_lookalike_audience(
    account: AdAccount,
    config: dict,
    existing: dict,
    dry_run: bool = True
) -> CustomAudience:
    """Maak lookalike audience aan"""
    name = config["name"]
    
    if name in existing:
        log(f"Audience bestaat al: {name} (ID: {existing[name]['id']})", "SKIP")
        return None
    
    # Check if source audience exists
    source_name = config["source_audience"]
    if source_name not in existing:
        log(f"Source audience niet gevonden: {source_name}", "WARNING")
        log(f"Maak eerst de source audience aan", "WARNING")
        return None
    
    source_id = existing[source_name]["id"]
    log(f"Aanmaken: {name} (van {source_name})", "CREATE")
    
    params = {
        CustomAudience.Field.name: name,
        CustomAudience.Field.description: config.get("description", ""),
        CustomAudience.Field.subtype: "LOOKALIKE",
        CustomAudience.Field.origin_audience_id: source_id,
        CustomAudience.Field.lookalike_spec: json.dumps({
            "type": "similarity",
            "country": config.get("country", "NL"),
            "ratio": config.get("ratio", 0.01),
        }),
    }
    
    if dry_run:
        log(f"[DRY RUN] Zou aanmaken: {name}")
        log(f"          Source: {source_name} (ID: {source_id})")
        log(f"          Ratio: {config.get('ratio', 0.01) * 100}%")
        return None
    
    try:
        audience = account.create_custom_audience(params=params)
        log(f"Aangemaakt: {name} (ID: {audience['id']})", "SUCCESS")
        return audience
    except Exception as e:
        log(f"Fout bij aanmaken {name}: {e}", "ERROR")
        return None


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def create_all_audiences(
    access_token: str,
    ad_account_id: str,
    pixel_id: str,
    page_id: str,
    dry_run: bool = True
):
    """Maak alle custom audiences aan"""
    
    log("=" * 60)
    log("META ADS CUSTOM AUDIENCES CREATOR")
    log(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log("=" * 60)
    
    if not dry_run:
        log("⚠️  WAARSCHUWING: LIVE MODE - Audiences worden aangemaakt!", "WARNING")
        response = input("Doorgaan? (ja/nee): ")
        if response.lower() != "ja":
            log("Afgebroken door gebruiker")
            return
    
    # Initialize
    account = initialize_api(access_token, ad_account_id)
    existing = get_existing_audiences(account)
    
    stats = {"created": 0, "skipped": 0, "failed": 0}
    
    # 1. Website Audiences
    log("\n" + "=" * 40)
    log("🌐 WEBSITE AUDIENCES (Pixel-based)")
    log("=" * 40)
    
    for config in WEBSITE_AUDIENCES:
        result = create_website_audience(account, config, pixel_id, existing, dry_run)
        if result:
            stats["created"] += 1
            existing[config["name"]] = {"id": result["id"]}
        elif config["name"] in existing:
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
    
    # 2. Event Audiences
    log("\n" + "=" * 40)
    log("🎯 EVENT AUDIENCES (Form interactions)")
    log("=" * 40)
    
    for config in EVENT_AUDIENCES:
        result = create_website_audience(account, config, pixel_id, existing, dry_run)
        if result:
            stats["created"] += 1
            existing[config["name"]] = {"id": result["id"]}
        elif config["name"] in existing:
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
    
    # 3. Video Audiences
    log("\n" + "=" * 40)
    log("🎬 VIDEO AUDIENCES")
    log("=" * 40)
    
    for config in VIDEO_AUDIENCES:
        result = create_engagement_audience(account, config, page_id, existing, dry_run)
        if result:
            stats["created"] += 1
            existing[config["name"]] = {"id": result["id"]}
        elif config["name"] in existing:
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
    
    # 4. Page Engagement Audiences
    log("\n" + "=" * 40)
    log("👥 PAGE ENGAGEMENT AUDIENCES")
    log("=" * 40)
    
    for config in ENGAGEMENT_AUDIENCES:
        result = create_engagement_audience(account, config, page_id, existing, dry_run)
        if result:
            stats["created"] += 1
            existing[config["name"]] = {"id": result["id"]}
        elif config["name"] in existing:
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
    
    # 5. Lookalike Audiences
    log("\n" + "=" * 40)
    log("🔄 LOOKALIKE AUDIENCES")
    log("=" * 40)
    
    # Refresh existing list after creating source audiences
    if not dry_run:
        existing = get_existing_audiences(account)
    
    for config in LOOKALIKE_CONFIGS:
        result = create_lookalike_audience(account, config, existing, dry_run)
        if result:
            stats["created"] += 1
        elif config["name"] in existing:
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
    
    # Summary
    log("\n" + "=" * 60)
    log("SAMENVATTING")
    log("=" * 60)
    log(f"✅ Aangemaakt: {stats['created']}")
    log(f"⏭️ Overgeslagen (bestaan al): {stats['skipped']}")
    log(f"❌ Mislukt: {stats['failed']}")
    
    if dry_run:
        log("\n💡 Dit was een DRY RUN.")
        log("   Voer uit met --live om audiences aan te maken.")


def show_audience_preview():
    """Toon preview van alle audiences"""
    log("=" * 60)
    log("CUSTOM AUDIENCES PREVIEW")
    log("=" * 60)
    
    log("\n🌐 WEBSITE AUDIENCES (Pixel-based)")
    log("-" * 40)
    for aud in WEBSITE_AUDIENCES:
        log(f"  • {aud['name']}")
        log(f"    Retention: {aud['retention_days']}d | Funnel: {aud.get('funnel_stage', 'N/A')}")
    
    log("\n🎯 EVENT AUDIENCES (Form interactions)")
    log("-" * 40)
    for aud in EVENT_AUDIENCES:
        log(f"  • {aud['name']}")
        log(f"    Retention: {aud['retention_days']}d | Use: {aud.get('use_for', 'targeting')}")
    
    log("\n🎬 VIDEO AUDIENCES")
    log("-" * 40)
    for aud in VIDEO_AUDIENCES:
        log(f"  • {aud['name']}")
        log(f"    Funnel: {aud.get('funnel_stage', 'N/A')}")
    
    log("\n👥 PAGE ENGAGEMENT AUDIENCES")
    log("-" * 40)
    for aud in ENGAGEMENT_AUDIENCES:
        log(f"  • {aud['name']}")
        log(f"    Retention: {aud['retention_days']}d")
    
    log("\n🔄 LOOKALIKE AUDIENCES")
    log("-" * 40)
    for aud in LOOKALIKE_CONFIGS:
        log(f"  • {aud['name']}")
        log(f"    Source: {aud['source_audience']} | Ratio: {aud['ratio']*100}%")
    
    # Funnel mapping
    log("\n" + "=" * 60)
    log("FUNNEL MAPPING")
    log("=" * 60)
    
    log("\n📊 Cold (TOFU) - Nieuwe prospects:")
    log("   → LAL 1% Website Visitors")
    log("   → LAL 1% Converters")
    log("   → Interest targeting")
    
    log("\n📊 Consider (MOFU) - Warme leads:")
    log("   → Video Viewers 50%+")
    log("   → Page Engagers 30d")
    log("   → Website Visitors 30d")
    
    log("\n📊 Retarget (BOFU) - Hot leads:")
    log("   → Website Visitors 14d")
    log("   → Website Visitors 7d")
    log("   → Form Starters")
    log("   → Video Viewers 95%")
    
    log("\n🚫 Exclusions:")
    log("   → KT - Converters (Leads) - exclude from all")


def list_existing_audiences(access_token: str, ad_account_id: str):
    """Lijst alle bestaande audiences"""
    account = initialize_api(access_token, ad_account_id)
    existing = get_existing_audiences(account)
    
    log("=" * 60)
    log("BESTAANDE CUSTOM AUDIENCES")
    log("=" * 60)
    
    # Filter KT audiences
    kt_audiences = {k: v for k, v in existing.items() if k.startswith("KT")}
    other_audiences = {k: v for k, v in existing.items() if not k.startswith("KT")}
    
    if kt_audiences:
        log("\n📁 Kandidatentekort Audiences:")
        for name, data in sorted(kt_audiences.items()):
            size = data.get("size", 0)
            log(f"  • {name}")
            log(f"    ID: {data['id']} | Size: {size:,}")
    
    if other_audiences:
        log(f"\n📁 Andere Audiences ({len(other_audiences)}):")
        for name, data in sorted(other_audiences.items())[:10]:
            log(f"  • {name} (ID: {data['id']})")
        if len(other_audiences) > 10:
            log(f"  ... en {len(other_audiences) - 10} meer")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Maak Meta Ads Custom Audiences voor Kandidatentekort.nl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  # Preview alle audiences
  python meta_ads_create_audiences.py --preview

  # Lijst bestaande audiences
  python meta_ads_create_audiences.py --list --token YOUR_TOKEN

  # Dry run
  python meta_ads_create_audiences.py --token YOUR_TOKEN --pixel 123 --page 456

  # Live aanmaken
  python meta_ads_create_audiences.py --token YOUR_TOKEN --pixel 123 --page 456 --live
        """
    )
    
    parser.add_argument(
        "--token",
        default=os.environ.get("META_ACCESS_TOKEN"),
        help="Facebook Marketing API access token"
    )
    
    parser.add_argument(
        "--account",
        default=os.environ.get("META_AD_ACCOUNT", "act_1236576254450117"),
        help="Ad Account ID"
    )
    
    parser.add_argument(
        "--pixel",
        default=os.environ.get("META_PIXEL_ID"),
        help="Meta Pixel ID voor website audiences"
    )
    
    parser.add_argument(
        "--page",
        default=os.environ.get("META_PAGE_ID"),
        help="Facebook Page ID voor engagement audiences"
    )
    
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Toon preview van audiences (geen API nodig)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lijst bestaande audiences"
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Live mode - maak audiences aan"
    )
    
    args = parser.parse_args()
    
    # Preview mode
    if args.preview:
        show_audience_preview()
        return
    
    # List mode
    if args.list:
        if not args.token:
            log("❌ Token nodig voor --list", "ERROR")
            sys.exit(1)
        list_existing_audiences(args.token, args.account)
        return
    
    # Validate params
    if not args.token:
        log("❌ Geen access token!", "ERROR")
        log("   Gebruik --preview voor preview zonder token")
        sys.exit(1)
    
    if not args.pixel:
        log("❌ Geen Pixel ID!", "ERROR")
        log("   Vind je Pixel ID in Events Manager > Data Sources")
        sys.exit(1)
    
    if not args.page:
        log("❌ Geen Page ID!", "ERROR")
        log("   Vind je Page ID op je Facebook Page > About")
        sys.exit(1)
    
    # Run
    create_all_audiences(
        access_token=args.token,
        ad_account_id=args.account,
        pixel_id=args.pixel,
        page_id=args.page,
        dry_run=not args.live
    )


if __name__ == "__main__":
    main()
