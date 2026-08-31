"""
Profession-based sleep questionnaire system
"""
import json
from datetime import datetime

def get_profession_questions(profession):
    """Get tailored questions based on user's profession"""
    
    # Base questions for all professions
    base_questions = [
        {
            "id": "sleep_duration",
            "question": "How many hours do you typically sleep per night?",
            "type": "number",
            "min": 3,
            "max": 12,
            "required": True
        },
        {
            "id": "sleep_quality",
            "question": "How would you rate your overall sleep quality?",
            "type": "select",
            "options": [
                {"value": 1, "label": "Very Poor"},
                {"value": 2, "label": "Poor"},
                {"value": 3, "label": "Fair"},
                {"value": 4, "label": "Good"},
                {"value": 5, "label": "Excellent"}
            ],
            "required": True
        },
        {
            "id": "bedtime",
            "question": "What time do you usually go to bed?",
            "type": "time",
            "required": True
        },
        {
            "id": "wake_time",
            "question": "What time do you usually wake up?",
            "type": "time",
            "required": True
        }
    ]
    
    # Profession-specific questions
    profession_questions = {
        "healthcare-worker": [
            {
                "id": "shift_type",
                "question": "What type of shifts do you work?",
                "type": "select",
                "options": [
                    {"value": "day", "label": "Day shifts (7am-7pm)"},
                    {"value": "night", "label": "Night shifts (7pm-7am)"},
                    {"value": "rotating", "label": "Rotating shifts"},
                    {"value": "on_call", "label": "On-call schedule"}
                ],
                "required": True
            },
            {
                "id": "shift_frequency",
                "question": "How many shifts do you work per week?",
                "type": "number",
                "min": 1,
                "max": 7,
                "required": True
            },
            {
                "id": "stress_level",
                "question": "How would you rate your work-related stress level?",
                "type": "select",
                "options": [
                    {"value": 1, "label": "Very Low"},
                    {"value": 2, "label": "Low"},
                    {"value": 3, "label": "Moderate"},
                    {"value": 4, "label": "High"},
                    {"value": 5, "label": "Very High"}
                ],
                "required": True
            },
            {
                "id": "caffeine_dependency",
                "question": "How often do you rely on caffeine to stay alert during work?",
                "type": "select",
                "options": [
                    {"value": "never", "label": "Never"},
                    {"value": "rarely", "label": "Rarely"},
                    {"value": "sometimes", "label": "Sometimes"},
                    {"value": "often", "label": "Often"},
                    {"value": "always", "label": "Always"}
                ],
                "required": True
            }
        ],
        
        "student": [
            {
                "id": "study_schedule",
                "question": "When do you typically study?",
                "type": "select",
                "options": [
                    {"value": "morning", "label": "Morning (6am-12pm)"},
                    {"value": "afternoon", "label": "Afternoon (12pm-6pm)"},
                    {"value": "evening", "label": "Evening (6pm-10pm)"},
                    {"value": "late_night", "label": "Late night (10pm-2am)"},
                    {"value": "all_nighter", "label": "All-nighters (2am+)"}
                ],
                "required": True
            },
            {
                "id": "exam_stress",
                "question": "How does exam stress affect your sleep?",
                "type": "select",
                "options": [
                    {"value": "no_effect", "label": "No effect"},
                    {"value": "slight_difficulty", "label": "Slight difficulty falling asleep"},
                    {"value": "frequent_waking", "label": "Frequent night wakings"},
                    {"value": "insomnia", "label": "Complete insomnia"},
                    {"value": "oversleeping", "label": "Oversleeping from exhaustion"}
                ],
                "required": True
            },
            {
                "id": "screen_time",
                "question": "How many hours do you spend on screens before bed?",
                "type": "number",
                "min": 0,
                "max": 8,
                "required": True
            },
            {
                "id": "social_activities",
                "question": "How often do social activities interfere with your sleep schedule?",
                "type": "select",
                "options": [
                    {"value": "never", "label": "Never"},
                    {"value": "rarely", "label": "Rarely"},
                    {"value": "sometimes", "label": "Sometimes"},
                    {"value": "often", "label": "Often"},
                    {"value": "always", "label": "Always"}
                ],
                "required": True
            }
        ],
        
        "shift-worker": [
            {
                "id": "shift_pattern",
                "question": "What is your shift pattern?",
                "type": "select",
                "options": [
                    {"value": "fixed_night", "label": "Fixed night shift"},
                    {"value": "fixed_day", "label": "Fixed day shift"},
                    {"value": "rotating_weekly", "label": "Rotating weekly"},
                    {"value": "rotating_monthly", "label": "Rotating monthly"},
                    {"value": "irregular", "label": "Irregular/unpredictable"}
                ],
                "required": True
            },
            {
                "id": "adaptation_difficulty",
                "question": "How difficult is it for you to adapt to shift changes?",
                "type": "select",
                "options": [
                    {"value": 1, "label": "Very Easy"},
                    {"value": 2, "label": "Easy"},
                    {"value": 3, "label": "Moderate"},
                    {"value": 4, "label": "Difficult"},
                    {"value": 5, "label": "Very Difficult"}
                ],
                "required": True
            },
            {
                "id": "sleep_aids",
                "question": "Do you use any sleep aids or medications?",
                "type": "select",
                "options": [
                    {"value": "none", "label": "None"},
                    {"value": "melatonin", "label": "Melatonin"},
                    {"value": "prescription", "label": "Prescription medication"},
                    {"value": "herbal", "label": "Herbal supplements"},
                    {"value": "multiple", "label": "Multiple aids"}
                ],
                "required": True
            }
        ],
        
        "remote-worker": [
            {
                "id": "work_location",
                "question": "Where do you primarily work from?",
                "type": "select",
                "options": [
                    {"value": "home_office", "label": "Dedicated home office"},
                    {"value": "bedroom", "label": "Bedroom"},
                    {"value": "living_room", "label": "Living room/common area"},
                    {"value": "various", "label": "Various locations"},
                    {"value": "coworking", "label": "Co-working spaces"}
                ],
                "required": True
            },
            {
                "id": "work_hours_flexibility",
                "question": "How flexible are your work hours?",
                "type": "select",
                "options": [
                    {"value": "very_flexible", "label": "Very flexible - I set my own schedule"},
                    {"value": "somewhat_flexible", "label": "Somewhat flexible - core hours required"},
                    {"value": "fixed", "label": "Fixed schedule like office work"},
                    {"value": "irregular", "label": "Irregular - depends on projects"}
                ],
                "required": True
            },
            {
                "id": "work_life_boundary",
                "question": "How well do you separate work and personal time?",
                "type": "select",
                "options": [
                    {"value": "excellent", "label": "Excellent - clear boundaries"},
                    {"value": "good", "label": "Good - mostly separate"},
                    {"value": "fair", "label": "Fair - some overlap"},
                    {"value": "poor", "label": "Poor - work bleeds into personal time"},
                    {"value": "no_boundary", "label": "No boundary - always available"}
                ],
                "required": True
            }
        ],
        
        "teacher-educator": [
            {
                "id": "grading_time",
                "question": "When do you typically do grading and lesson planning?",
                "type": "select",
                "options": [
                    {"value": "school_hours", "label": "During school hours"},
                    {"value": "early_evening", "label": "Early evening (5-8pm)"},
                    {"value": "late_evening", "label": "Late evening (8-11pm)"},
                    {"value": "late_night", "label": "Late night (after 11pm)"},
                    {"value": "weekends", "label": "Primarily weekends"}
                ],
                "required": True
            },
            {
                "id": "school_stress",
                "question": "How does school-related stress affect your sleep?",
                "type": "select",
                "options": [
                    {"value": "no_effect", "label": "No effect"},
                    {"value": "occasional", "label": "Occasional sleep disruption"},
                    {"value": "frequent", "label": "Frequent sleep problems"},
                    {"value": "severe", "label": "Severe insomnia"},
                    {"value": "seasonal", "label": "Worse during certain times of year"}
                ],
                "required": True
            }
        ],
        
        "engineer-tech": [
            {
                "id": "coding_hours",
                "question": "How many hours per day do you spend coding/on technical work?",
                "type": "number",
                "min": 1,
                "max": 16,
                "required": True
            },
            {
                "id": "late_night_coding",
                "question": "How often do you code late into the night?",
                "type": "select",
                "options": [
                    {"value": "never", "label": "Never"},
                    {"value": "rarely", "label": "Rarely"},
                    {"value": "sometimes", "label": "Sometimes"},
                    {"value": "often", "label": "Often"},
                    {"value": "always", "label": "Almost every night"}
                ],
                "required": True
            },
            {
                "id": "blue_light_exposure",
                "question": "Do you use blue light filters or glasses?",
                "type": "select",
                "options": [
                    {"value": "always", "label": "Always use filters/glasses"},
                    {"value": "sometimes", "label": "Sometimes"},
                    {"value": "rarely", "label": "Rarely"},
                    {"value": "never", "label": "Never"}
                ],
                "required": True
            }
        ]
    }
    
    # Get profession-specific questions or default to general questions
    specific_questions = profession_questions.get(profession, [
        {
            "id": "work_stress",
            "question": "How would you rate your work-related stress level?",
            "type": "select",
            "options": [
                {"value": 1, "label": "Very Low"},
                {"value": 2, "label": "Low"},
                {"value": 3, "label": "Moderate"},
                {"value": 4, "label": "High"},
                {"value": 5, "label": "Very High"}
            ],
            "required": True
        },
        {
            "id": "work_hours",
            "question": "How many hours do you work per day on average?",
            "type": "number",
            "min": 1,
            "max": 16,
            "required": True
        }
    ])
    
    # Additional common questions
    common_questions = [
        {
            "id": "exercise_frequency",
            "question": "How often do you exercise per week?",
            "type": "select",
            "options": [
                {"value": 0, "label": "Never"},
                {"value": 1, "label": "1-2 times"},
                {"value": 2, "label": "3-4 times"},
                {"value": 3, "label": "5-6 times"},
                {"value": 4, "label": "Daily"}
            ],
            "required": True
        },
        {
            "id": "caffeine_intake",
            "question": "How many cups of coffee/tea do you drink per day?",
            "type": "number",
            "min": 0,
            "max": 10,
            "required": True
        },
        {
            "id": "sleep_environment",
            "question": "How would you rate your sleep environment?",
            "type": "select",
            "options": [
                {"value": 1, "label": "Very Poor (noisy, bright, uncomfortable)"},
                {"value": 2, "label": "Poor"},
                {"value": 3, "label": "Fair"},
                {"value": 4, "label": "Good"},
                {"value": 5, "label": "Excellent (dark, quiet, comfortable)"}
            ],
            "required": True
        }
    ]
    
    return {
        "profession": profession,
        "questions": base_questions + specific_questions + common_questions
    }

def analyze_sleep_responses(responses, user_profession):
    """Analyze user responses and provide personalized recommendations"""
    
    # Calculate sleep score
    sleep_score = calculate_sleep_score(responses, user_profession)
    
    # Generate recommendations
    recommendations = generate_profession_recommendations(responses, user_profession)
    
    # Identify risk factors
    risk_factors = identify_risk_factors(responses, user_profession)
    
    # Generate insights
    insights = generate_insights(responses, user_profession)
    
    return {
        "sleep_score": sleep_score,
        "sleep_grade": get_sleep_grade(sleep_score),
        "recommendations": recommendations,
        "risk_factors": risk_factors,
        "insights": insights,
        "profession_specific_advice": get_profession_advice(user_profession, responses)
    }

def calculate_sleep_score(responses, profession):
    """Calculate overall sleep score based on responses"""
    score = 0
    max_score = 100
    
    # Sleep duration scoring (30 points)
    sleep_duration = float(responses.get('sleep_duration', 7))
    if 7 <= sleep_duration <= 9:
        score += 30
    elif 6 <= sleep_duration < 7 or 9 < sleep_duration <= 10:
        score += 20
    elif 5 <= sleep_duration < 6 or 10 < sleep_duration <= 11:
        score += 10
    else:
        score += 0
    
    # Sleep quality scoring (25 points)
    sleep_quality = int(responses.get('sleep_quality', 3))
    score += (sleep_quality - 1) * 6.25
    
    # Sleep environment scoring (15 points)
    sleep_env = int(responses.get('sleep_environment', 3))
    score += (sleep_env - 1) * 3.75
    
    # Exercise frequency scoring (10 points)
    exercise = int(responses.get('exercise_frequency', 1))
    score += exercise * 2.5
    
    # Caffeine intake scoring (10 points) - reverse scoring
    caffeine = int(responses.get('caffeine_intake', 2))
    if caffeine <= 2:
        score += 10
    elif caffeine <= 4:
        score += 5
    else:
        score += 0
    
    # Profession-specific adjustments (10 points)
    profession_score = get_profession_score(responses, profession)
    score += profession_score
    
    return min(max(score, 0), 100)

def get_profession_score(responses, profession):
    """Get profession-specific score adjustments"""
    score = 0
    
    if profession == "healthcare-worker":
        shift_type = responses.get('shift_type', 'day')
        if shift_type == 'night':
            score -= 5
        elif shift_type == 'rotating':
            score -= 3
        
        stress_level = int(responses.get('stress_level', 3))
        score -= (stress_level - 1) * 1.25
    
    elif profession == "student":
        study_schedule = responses.get('study_schedule', 'evening')
        if study_schedule in ['late_night', 'all_nighter']:
            score -= 5
        
        screen_time = int(responses.get('screen_time', 2))
        if screen_time > 3:
            score -= 3
    
    elif profession == "shift-worker":
        adaptation = int(responses.get('adaptation_difficulty', 3))
        score -= (adaptation - 1) * 1.5
    
    elif profession == "remote-worker":
        boundary = responses.get('work_life_boundary', 'fair')
        if boundary in ['poor', 'no_boundary']:
            score -= 4
        elif boundary == 'excellent':
            score += 2
    
    return max(score, -10)

def get_sleep_grade(score):
    """Convert sleep score to letter grade"""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    elif score >= 50:
        return "C-"
    elif score >= 45:
        return "D+"
    elif score >= 40:
        return "D"
    else:
        return "F"

def generate_profession_recommendations(responses, profession):
    """Generate profession-specific recommendations"""
    recommendations = []
    
    # Base recommendations
    sleep_duration = float(responses.get('sleep_duration', 7))
    if sleep_duration < 7:
        recommendations.append("Aim for 7-9 hours of sleep per night for optimal health and performance.")
    
    sleep_quality = int(responses.get('sleep_quality', 3))
    if sleep_quality < 4:
        recommendations.append("Focus on improving sleep quality through better sleep hygiene practices.")
    
    # Profession-specific recommendations
    if profession == "healthcare-worker":
        shift_type = responses.get('shift_type', 'day')
        if shift_type == 'night':
            recommendations.extend([
                "Use blackout curtains and eye masks to create darkness for daytime sleep.",
                "Consider strategic caffeine use - avoid 6 hours before planned sleep time.",
                "Try to maintain consistent sleep schedule even on days off."
            ])
        elif shift_type == 'rotating':
            recommendations.extend([
                "Gradually adjust sleep time 2-3 days before shift changes.",
                "Use light therapy to help reset your circadian rhythm.",
                "Consider short naps (20-30 minutes) during breaks if possible."
            ])
    
    elif profession == "student":
        study_schedule = responses.get('study_schedule', 'evening')
        if study_schedule in ['late_night', 'all_nighter']:
            recommendations.extend([
                "Try to shift study time earlier in the day for better sleep quality.",
                "Use the Pomodoro technique to study more efficiently in less time.",
                "Create a consistent study schedule to avoid last-minute cramming."
            ])
        
        screen_time = int(responses.get('screen_time', 2))
        if screen_time > 2:
            recommendations.extend([
                "Implement a digital curfew 1-2 hours before bedtime.",
                "Use blue light filters on devices after sunset.",
                "Replace screen time with relaxing activities like reading or meditation."
            ])
    
    elif profession == "shift-worker":
        recommendations.extend([
            "Maintain a consistent sleep schedule even on days off when possible.",
            "Use strategic light exposure to help adjust your circadian rhythm.",
            "Consider split sleep schedules if single long sleep periods are difficult."
        ])
    
    elif profession == "remote-worker":
        work_location = responses.get('work_location', 'home_office')
        if work_location == 'bedroom':
            recommendations.append("Avoid working in your bedroom to maintain sleep-wake associations.")
        
        boundary = responses.get('work_life_boundary', 'fair')
        if boundary in ['poor', 'no_boundary']:
            recommendations.extend([
                "Establish clear work hours and stick to them.",
                "Create a shutdown ritual to transition from work to personal time.",
                "Use separate devices or accounts for work and personal activities."
            ])
    
    elif profession == "teacher-educator":
        grading_time = responses.get('grading_time', 'early_evening')
        if grading_time in ['late_evening', 'late_night']:
            recommendations.extend([
                "Try to complete grading and planning earlier in the day.",
                "Use efficient grading techniques to reduce time spent.",
                "Set boundaries on work hours to protect sleep time."
            ])
    
    elif profession == "engineer-tech":
        late_coding = responses.get('late_night_coding', 'sometimes')
        if late_coding in ['often', 'always']:
            recommendations.extend([
                "Set a hard cutoff time for coding to protect sleep.",
                "Use time-blocking to ensure work fits within reasonable hours.",
                "Take regular breaks to prevent getting 'in the zone' too late."
            ])
        
        blue_light = responses.get('blue_light_exposure', 'sometimes')
        if blue_light in ['rarely', 'never']:
            recommendations.append("Use blue light filters or glasses, especially in the evening.")
    
    return recommendations

def identify_risk_factors(responses, profession):
    """Identify potential sleep risk factors"""
    risk_factors = []
    
    # General risk factors
    sleep_duration = float(responses.get('sleep_duration', 7))
    if sleep_duration < 6:
        risk_factors.append("Chronic sleep deprivation (less than 6 hours)")
    elif sleep_duration > 10:
        risk_factors.append("Excessive sleep duration (may indicate underlying issues)")
    
    caffeine = int(responses.get('caffeine_intake', 2))
    if caffeine > 4:
        risk_factors.append("High caffeine intake (may interfere with sleep)")
    
    exercise = int(responses.get('exercise_frequency', 1))
    if exercise == 0:
        risk_factors.append("Sedentary lifestyle (lack of exercise affects sleep quality)")
    
    # Profession-specific risk factors
    if profession == "healthcare-worker":
        stress_level = int(responses.get('stress_level', 3))
        if stress_level >= 4:
            risk_factors.append("High work-related stress")
        
        shift_type = responses.get('shift_type', 'day')
        if shift_type in ['night', 'rotating']:
            risk_factors.append("Shift work sleep disorder risk")
    
    elif profession == "student":
        exam_stress = responses.get('exam_stress', 'no_effect')
        if exam_stress in ['insomnia', 'frequent_waking']:
            risk_factors.append("Stress-induced sleep disorders")
        
        screen_time = int(responses.get('screen_time', 2))
        if screen_time > 3:
            risk_factors.append("Excessive screen time before bed")
    
    elif profession == "shift-worker":
        adaptation = int(responses.get('adaptation_difficulty', 3))
        if adaptation >= 4:
            risk_factors.append("Difficulty adapting to shift changes")
    
    return risk_factors

def generate_insights(responses, profession):
    """Generate personalized insights"""
    insights = []
    
    # Sleep timing insights
    bedtime = responses.get('bedtime', '22:00')
    wake_time = responses.get('wake_time', '07:00')
    sleep_duration = float(responses.get('sleep_duration', 7))
    
    # Convert times to calculate sleep window
    bed_hour = int(bedtime.split(':')[0])
    wake_hour = int(wake_time.split(':')[0])
    
    if bed_hour > 23 or bed_hour < 6:
        insights.append("Your bedtime is quite late. Earlier bedtimes are associated with better sleep quality and improved circadian rhythm alignment.")
    
    if sleep_duration < 7:
        insights.append(f"At {sleep_duration} hours per night, you're getting less than the recommended 7-9 hours of sleep. This may impact your cognitive performance, immune function, and overall health.")
    elif sleep_duration > 9:
        insights.append(f"You're sleeping {sleep_duration} hours per night, which is on the higher end. While some people need more sleep, excessive sleep can sometimes indicate underlying health issues.")
    
    # Caffeine insights
    caffeine = int(responses.get('caffeine_intake', 2))
    if caffeine > 3:
        insights.append(f"Your caffeine intake of {caffeine} cups per day is quite high. Consider reducing intake, especially after 2 PM, as caffeine can stay in your system for 6-8 hours.")
    
    # Exercise insights
    exercise = int(responses.get('exercise_frequency', 1))
    if exercise == 0:
        insights.append("Regular exercise can significantly improve sleep quality by helping regulate your circadian rhythm and reducing stress levels.")
    elif exercise >= 3:
        insights.append("Your regular exercise routine is excellent for sleep quality. Just ensure you're not exercising too close to bedtime.")
    
    # Profession-specific insights
    profession_insights = {
        "healthcare-worker": "Healthcare workers often struggle with irregular sleep patterns due to shift work. Your responses suggest focusing on sleep hygiene during off-hours and strategic napping during long shifts could be beneficial.",
        "student": "Students frequently sacrifice sleep for academic performance, but research shows that adequate sleep actually improves learning, memory consolidation, and academic outcomes. Quality sleep is an investment in your academic success.",
        "shift-worker": "Shift workers face unique challenges with circadian rhythm disruption. Your responses indicate that strategic light exposure and consistent sleep routines during your available sleep windows could help minimize these effects.",
        "remote-worker": "Remote workers have the advantage of flexible schedules but may struggle with work-life boundaries affecting sleep. Creating physical and temporal boundaries between work and rest is crucial for quality sleep.",
        "teacher-educator": "Teachers often experience seasonal stress patterns that can affect sleep. Managing workload and stress during busy periods (like grading seasons and parent conferences) is important for maintaining consistent sleep quality.",
        "engineer-tech": "Tech professionals often experience 'flow states' that can extend work hours into sleep time. Setting boundaries and using blue light management strategies are crucial for long-term productivity and health."
    }
    
    if profession in profession_insights:
        insights.append(profession_insights[profession])
    
    # Add profession-specific behavioral insights
    if profession == "healthcare-worker":
        shift_type = responses.get('shift_type', 'day')
        if shift_type == 'night':
            insights.append("Night shift work can reduce sleep quality by 20-30%. Consider blackout curtains, white noise machines, and maintaining consistent sleep schedules even on days off.")
        elif shift_type == 'rotating':
            insights.append("Rotating shifts are particularly challenging for sleep. Your body may never fully adapt, so focus on sleep hygiene and consider light therapy to help with transitions.")
    
    elif profession == "student":
        study_schedule = responses.get('study_schedule', 'evening')
        if study_schedule in ['late_night', 'all_nighter']:
            insights.append("Late-night studying can create a cycle of sleep debt. Research shows that sleep after learning helps consolidate memories, making adequate sleep crucial for academic performance.")
        
        screen_time = int(responses.get('screen_time', 2))
        if screen_time > 2:
            insights.append(f"Your {screen_time} hours of pre-bedtime screen time may be suppressing melatonin production. Blue light exposure can delay sleep onset by 30-60 minutes.")
    
    elif profession == "remote-worker":
        work_location = responses.get('work_location', 'home_office')
        if work_location == 'bedroom':
            insights.append("Working in your bedroom can create negative sleep associations. Your brain may start associating the bedroom with work stress rather than rest and relaxation.")
        
        boundary = responses.get('work_life_boundary', 'fair')
        if boundary in ['poor', 'no_boundary']:
            insights.append("Poor work-life boundaries can lead to chronic stress and sleep disruption. Consider implementing a 'shutdown ritual' to mentally transition from work to personal time.")
    
    return insights

def get_profession_advice(profession, responses):
    """Get specific advice for the user's profession"""
    advice = {
        "healthcare-worker": {
            "title": "Healthcare Worker Sleep Optimization",
            "tips": [
                "Use strategic napping (20-30 minutes) during long shifts",
                "Maintain consistent meal times to support circadian rhythm",
                "Consider melatonin supplementation (consult with physician)",
                "Use compression socks and comfortable shoes to reduce physical fatigue"
            ]
        },
        "student": {
            "title": "Student Sleep Success Strategies",
            "tips": [
                "Schedule study time in blocks with breaks to avoid late-night cramming",
                "Use active recall and spaced repetition for more efficient studying",
                "Create a pre-exam sleep routine to manage stress",
                "Join study groups to share workload and reduce individual stress"
            ]
        },
        "shift-worker": {
            "title": "Shift Worker Sleep Management",
            "tips": [
                "Use bright light exposure at the beginning of your shift",
                "Wear sunglasses on the drive home to signal sleep time",
                "Consider split sleep schedules if single sleep periods don't work",
                "Communicate your sleep schedule to family/roommates for support"
            ]
        },
        "remote-worker": {
            "title": "Remote Worker Sleep Boundaries",
            "tips": [
                "Create a dedicated workspace separate from your bedroom",
                "Use different user accounts for work and personal activities",
                "Establish 'commute' rituals to transition between work and personal time",
                "Set automatic email/message delays to avoid late-night work communications"
            ]
        },
        "teacher-educator": {
            "title": "Educator Sleep & Stress Management",
            "tips": [
                "Batch similar tasks (grading, lesson planning) for efficiency",
                "Use voice-to-text for faster feedback on student work",
                "Set specific hours for school-related work and stick to them",
                "Practice stress-reduction techniques during busy periods (testing, report cards)"
            ]
        },
        "engineer-tech": {
            "title": "Tech Professional Sleep Hygiene",
            "tips": [
                "Use the Pomodoro Technique to prevent extended coding sessions",
                "Set up automatic blue light filters that activate at sunset",
                "Use 'Do Not Disturb' modes on devices after work hours",
                "Practice the '2-minute rule' - if debugging will take more than 2 minutes, save it for tomorrow"
            ]
        }
    }
    
    return advice.get(profession, {
        "title": "General Sleep Optimization",
        "tips": [
            "Maintain consistent sleep and wake times",
            "Create a relaxing bedtime routine",
            "Optimize your sleep environment (cool, dark, quiet)",
            "Limit caffeine intake, especially in the afternoon and evening"
        ]
    })