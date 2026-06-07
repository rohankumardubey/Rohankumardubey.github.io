from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer


OUTPUT = Path("output/pdf/Rohan_DE_updated.pdf")


def build_styles():
    styles = getSampleStyleSheet()
    blue = colors.HexColor("#1f5fbf")
    dark = colors.HexColor("#1e1e1e")
    muted = colors.HexColor("#586174")
    rule = colors.HexColor("#d8e2f3")

    styles.add(
        ParagraphStyle(
            name="Name",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=24,
            textColor=blue,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Contact",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=10.2,
            textColor=muted,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.1,
            leading=11.5,
            textColor=blue,
            spaceBefore=4,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Summary",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10.2,
            textColor=dark,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletLine",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.25,
            leading=9.6,
            textColor=dark,
            leftIndent=0,
            spaceAfter=1.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="RoleTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.9,
            leading=10.2,
            textColor=blue,
            spaceAfter=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="RoleMeta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.9,
            leading=9.0,
            textColor=muted,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="RoleBullet",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.85,
            leading=9.15,
            textColor=dark,
            leftIndent=0,
            spaceAfter=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Project",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.05,
            leading=9.3,
            textColor=dark,
            spaceAfter=1.2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterLine",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.0,
            leading=9.2,
            textColor=dark,
        )
    )
    return styles, rule


def paragraph(text, style):
    return Paragraph(text.replace("&", "&amp;"), style)


def role_block(styles, title, meta, bullets):
    items = [
        paragraph(title, styles["RoleTitle"]),
        paragraph(meta, styles["RoleMeta"]),
    ]
    for bullet in bullets:
        items.append(paragraph(f"- {bullet}", styles["RoleBullet"]))
    items.append(Spacer(1, 2))
    items.append(HRFlowable(color=colors.HexColor("#d8e2f3"), thickness=0.6, spaceBefore=1, spaceAfter=5))
    return KeepTogether(items)


def build_resume():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles, rule = build_styles()

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        topMargin=0.5 * inch,
        bottomMargin=0.42 * inch,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
    )

    story = []

    story.append(paragraph("Rohan Dubey", styles["Name"]))
    story.append(
        paragraph(
            "Hyderabad, India | +91-7093123447 | rohankumardubey497@gmail.com | github.com/Rohan-flutterint | rohan-flutterint.github.io",
            styles["Contact"],
        )
    )
    story.append(Spacer(1, 4))
    story.append(HRFlowable(color=rule, thickness=1, width="100%", spaceBefore=0, spaceAfter=8))

    story.append(paragraph("SUMMARY", styles["Section"]))
    story.append(
        paragraph(
            "Lead Data Engineer with hands-on depth in real-time, low-latency distributed systems and cost-efficient AWS data platforms. "
            "Over 8 years building production pipelines with Flink, Kafka/MSK, Kinesis Data Analytics, Spark, DynamoDB, and S3, with a track record in performance tuning, reliability, and cloud cost optimization.",
            styles["Summary"],
        )
    )

    story.append(paragraph("CORE STRENGTHS", styles["Section"]))
    core_lines = [
        "Languages: Java, Python, Go, Scala, C++, SQL, Shell.",
        "Streaming & Batch: Apache Flink, Kafka (MSK), Spark, Kinesis Data Analytics, Airflow.",
        "Storage & Databases: DynamoDB, PostgreSQL, MySQL, Apache Iceberg, Delta Lake, Parquet/ORC, S3.",
        "Infra & Cloud: AWS (S3, Glue, EMR, KDA, MSK, Redshift, Athena), Kubernetes, Docker.",
        "Specialties: Exactly-once processing, checkpointing, schema evolution, observability, runtime tuning, and cost optimization.",
    ]
    for line in core_lines:
        story.append(paragraph(f"- {line}", styles["BulletLine"]))

    story.append(paragraph("EXPERIENCE", styles["Section"]))
    roles = [
        (
            "Flutter Entertainment - Lead Data Engineer, Enterprise Tech",
            "Jun 2026 - Present, Hyderabad",
            [
                "Moved into Enterprise Tech to support broader company-wide data and platform initiatives across Flutter Entertainment.",
                "Applying production discipline from Streaming AI to enterprise-facing data workflows with a focus on reliability, clarity, and scalable delivery.",
            ],
        ),
        (
            "PokerStars - Lead Big Data Engineer, Streaming AI",
            "Jan 2026 - Jun 2026, Hyderabad",
            [
                "Promoted to lead the Streaming AI data engineering track, guiding architecture and delivery for real-time workloads on AWS.",
                "Improved runtime behavior and infrastructure efficiency through hot-path IO reduction, storage layout tuning, and stronger recovery strategy.",
            ],
        ),
        (
            "PokerStars - Senior Big Data Engineer, Streaming AI",
            "Aug 2023 - Jan 2026, Hyderabad",
            [
                "Designed real-time processing on AWS using Flink on Kinesis Data Analytics, MSK, DynamoDB, and S3 for high-value production workloads.",
                "Cut hot-path IO and delivered major annual cost savings through DynamoDB modeling, payload compaction, and S3 layout tuning.",
                "Built exactly-once sinks with checkpoint alignment and idempotent upserts while tuning RocksDB state and JVM behavior for recovery and latency.",
            ],
        ),
        (
            "Experian PLC - Senior Data Engineer",
            "Mar 2023 - Aug 2023, Hyderabad",
            [
                "Delivered regulated pipelines with secure ingestion, data quality gates, and lineage to accelerate analytics readiness for clients.",
                "Standardized batch and streaming jobs with reproducible configuration and monitoring.",
            ],
        ),
        (
            "Model N - Member of Technical Staff 3",
            "Jun 2021 - Mar 2023, Hyderabad",
            [
                "Built event-driven analytics with Kafka, Spark, and Delta Lake; exposed downstream access through Dremio and REST services.",
                "Improved query performance with partitioning, Z-ordering, predicate pushdown, and compaction to reduce compute and storage cost.",
            ],
        ),
        (
            "Carelon Global Solutions - Software Engineer",
            "Aug 2020 - Jun 2021, Hyderabad",
            [
                "Integrated Medicare and Medicaid datasets with SQL analytics to improve revenue capture and reduce operational overhead.",
            ],
        ),
        (
            "Legato Health Technologies - Associate Software Engineer",
            "Jul 2018 - Aug 2020, Hyderabad",
            [
                "Delivered optimized ETL on Teradata and Informatica while standardizing SLAs, validations, and delivery quality.",
            ],
        ),
    ]
    for title, meta, bullets in roles:
        story.append(role_block(styles, title, meta, bullets))

    story.append(paragraph("SELECTED PROJECTS", styles["Section"]))
    project_lines = [
        "GoXStream: Flink-inspired stream processor in Go with operator graphs, checkpoints, and Kafka, file, and database connectors (github.com/Rohan-flutterint/goxstream).",
        "FlowCore: Rust-based real-time stream processor inspired by Apache Flink with event-time windows, watermarks, late-event handling, checkpointing, and a live dashboard (github.com/Rohan-flutterint/FlowCore).",
    ]
    for line in project_lines:
        story.append(paragraph(f"- {line}", styles["Project"]))

    story.append(paragraph("EDUCATION", styles["Section"]))
    story.append(
        paragraph(
            "Jawaharlal Nehru Technological University, Hyderabad - B.Tech in Electrical Engineering, GPA 4.0/4.0 (2014 - 2018)",
            styles["FooterLine"],
        )
    )

    story.append(paragraph("KEYWORDS (ATS)", styles["Section"]))
    story.append(
        paragraph(
            "Distributed Systems, Real-time Streaming, Low Latency, Apache Kafka, Apache Flink, Apache Spark, AWS, DynamoDB, MSK, Kinesis, Kubernetes, Docker, CI/CD, Java, Python, Go, SQL, Parquet/ORC, Observability, Exactly-Once, Checkpointing, Data Modeling, Cost Optimization, Data Lake, Athena, PostgreSQL, AWS Glue, Apache Iceberg, Jenkins, Bitbucket, Teradata, GCP, BigQuery.",
            styles["FooterLine"],
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_resume()
