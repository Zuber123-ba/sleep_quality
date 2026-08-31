def get_recommendations(data, label):
    recommendations = []

    if label == "Bad":
        recommendations = [
            "Sleep at least 7–9 hours every night",
            "Reduce stress using meditation or breathing exercises",
            "Avoid caffeine after evening",
            "Reduce screen time before bed",
            "Maintain a fixed sleep schedule",
            "Exercise regularly but not late at night"
        ]

    elif label == "Good":
        recommendations = [
            "Maintain your current sleep routine",
            "Try to reduce screen time before sleep",
            "Limit caffeine intake",
            "Keep stress levels low",
            "Continue regular exercise"
        ]

    elif label == "Best":
        recommendations = [
            "Excellent sleep habits!",
            "Maintain consistency in sleep schedule",
            "Continue balanced diet and exercise",
            "Keep managing stress effectively",
            "Avoid unnecessary late-night screen usage"
        ]

    return recommendations
