from app.llm_classifier import classify_vendor

result = classify_vendor(
    vendor="Figma",
    description="Design collaboration software"
)

print(result)