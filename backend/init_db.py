"""
Initialize database with seed data
"""
from app.db.base import SessionLocal, engine, Base
from app.models.moderation_rule import ModerationRule, RuleType, Region
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database with seed data"""

    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if rules already exist
        existing_rules = db.query(ModerationRule).count()
        if existing_rules > 0:
            logger.info(f"Database already has {existing_rules} rules. Skipping seed data.")
            return

        logger.info("Adding seed data...")

        # Create default rules
        rules = [
            # Global toxicity rule
            ModerationRule(
                name="Global Toxicity Detection",
                description="Detect toxic, offensive, and hate speech content",
                rule_type=RuleType.TOXICITY,
                region=Region.GLOBAL,
                threshold=0.7,
                is_active=True,
                priority=100,
                created_by="system"
            ),

            # Global PII detection
            ModerationRule(
                name="Global PII Detection",
                description="Detect personally identifiable information",
                rule_type=RuleType.PII,
                region=Region.GLOBAL,
                is_active=True,
                priority=90,
                created_by="system"
            ),

            # US - HIPAA medical terms
            ModerationRule(
                name="US HIPAA Medical Terms",
                description="Block medical diagnosis and treatment information for US region",
                rule_type=RuleType.MEDICAL,
                region=Region.US,
                patterns=[
                    "diagnosis", "prescription", "medication dosage",
                    "medical condition", "treatment plan", "symptom diagnosis"
                ],
                is_active=True,
                priority=80,
                created_by="system"
            ),

            # EU - GDPR compliance
            ModerationRule(
                name="EU GDPR Data Protection",
                description="Enhanced PII detection for EU GDPR compliance",
                rule_type=RuleType.PII,
                region=Region.EU,
                is_active=True,
                priority=85,
                created_by="system"
            ),

            # Financial terms
            ModerationRule(
                name="Restricted Financial Advice",
                description="Block specific investment advice and financial predictions",
                rule_type=RuleType.FINANCIAL,
                region=Region.GLOBAL,
                patterns=[
                    "guaranteed return", "risk-free investment",
                    "insider trading", "pump and dump",
                    "get rich quick", "investment guarantee"
                ],
                is_active=True,
                priority=70,
                created_by="system"
            ),

            # Hate speech keywords
            ModerationRule(
                name="Hate Speech Keywords",
                description="Block known hate speech terms and slurs",
                rule_type=RuleType.KEYWORD,
                region=Region.GLOBAL,
                patterns=[
                    # Add appropriate patterns here
                    "extremist", "violent threat"
                ],
                is_active=True,
                priority=95,
                created_by="system"
            ),

            # Cryptocurrency scams
            ModerationRule(
                name="Cryptocurrency Scam Detection",
                description="Detect common cryptocurrency scam patterns",
                rule_type=RuleType.KEYWORD,
                region=Region.GLOBAL,
                patterns=[
                    "send bitcoin", "double your crypto",
                    "free cryptocurrency", "crypto giveaway scam"
                ],
                is_active=True,
                priority=75,
                created_by="system"
            )
        ]

        for rule in rules:
            db.add(rule)

        db.commit()
        logger.info(f"Successfully added {len(rules)} seed rules")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization complete!")
