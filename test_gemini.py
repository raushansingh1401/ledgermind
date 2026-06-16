from app.llm_classifier import classify_vendor

print(
    classify_vendor(
        vendor="Figma",
        description="Design collaboration software"
    )
)