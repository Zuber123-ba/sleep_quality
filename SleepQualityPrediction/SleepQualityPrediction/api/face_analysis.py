"""
Advanced face analysis for sleep quality assessment
"""
import base64
import io
import os
from PIL import Image, ImageStat, ImageFilter, ImageEnhance
import json
from datetime import datetime

def analyze_face_image(image_data, user_info=None):
    """
    Analyze uploaded face image for sleep quality indicators
    """
    try:
        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform various analyses
        analysis_results = {
            'overall_fatigue_score': 0,
            'eye_analysis': analyze_eye_region(image),
            'skin_analysis': analyze_skin_condition(image),
            'facial_symmetry': analyze_facial_symmetry(image),
            'color_analysis': analyze_facial_colors(image),
            'brightness_analysis': analyze_image_brightness(image),
            'recommendations': [],
            'detailed_insights': [],
            'sleep_quality_indicators': {}
        }
        
        # Calculate overall fatigue score
        analysis_results['overall_fatigue_score'] = calculate_fatigue_score(analysis_results)
        
        # Generate recommendations based on analysis
        analysis_results['recommendations'] = generate_face_recommendations(analysis_results, user_info)
        
        # Generate detailed insights
        analysis_results['detailed_insights'] = generate_face_insights(analysis_results)
        
        # Determine sleep quality indicators
        analysis_results['sleep_quality_indicators'] = determine_sleep_indicators(analysis_results)
        
        return {
            'success': True,
            'analysis': analysis_results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def analyze_eye_region(image):
    """
    Analyze eye region for fatigue indicators
    """
    width, height = image.size
    
    # Estimate eye region (upper third of face, middle section)
    eye_region = image.crop((
        int(width * 0.2),  # left
        int(height * 0.3), # top
        int(width * 0.8),  # right
        int(height * 0.6)  # bottom
    ))
    
    # Analyze eye region characteristics
    eye_stats = ImageStat.Stat(eye_region)
    
    # Convert to grayscale for better analysis
    eye_gray = eye_region.convert('L')
    eye_gray_stats = ImageStat.Stat(eye_gray)
    
    # Detect potential dark circles (darker areas under eyes)
    lower_eye_region = image.crop((
        int(width * 0.25),
        int(height * 0.5),
        int(width * 0.75),
        int(height * 0.65)
    ))
    
    lower_eye_gray = lower_eye_region.convert('L')
    lower_eye_stats = ImageStat.Stat(lower_eye_gray)
    
    # Calculate metrics
    eye_brightness = eye_gray_stats.mean[0]
    lower_eye_brightness = lower_eye_stats.mean[0]
    
    # Dark circle indicator (lower region darker than upper)
    dark_circle_intensity = max(0, eye_brightness - lower_eye_brightness)
    
    # Puffiness indicator (based on color variation)
    color_variation = eye_stats.stddev[0] + eye_stats.stddev[1] + eye_stats.stddev[2]
    
    return {
        'eye_brightness': eye_brightness,
        'dark_circle_intensity': dark_circle_intensity,
        'puffiness_indicator': color_variation,
        'fatigue_score': calculate_eye_fatigue_score(eye_brightness, dark_circle_intensity, color_variation)
    }

def analyze_skin_condition(image):
    """
    Analyze overall skin condition and complexion
    """
    # Analyze overall skin tone and condition
    skin_stats = ImageStat.Stat(image)
    
    # Convert to different color spaces for analysis
    hsv_image = image.convert('HSV')
    hsv_stats = ImageStat.Stat(hsv_image)
    
    # Analyze skin smoothness using edge detection
    gray_image = image.convert('L')
    edges = gray_image.filter(ImageFilter.FIND_EDGES)
    edge_stats = ImageStat.Stat(edges)
    
    # Calculate skin health indicators
    skin_brightness = skin_stats.mean[0] + skin_stats.mean[1] + skin_stats.mean[2]
    skin_saturation = hsv_stats.mean[1]
    skin_smoothness = 255 - edge_stats.mean[0]  # Inverse of edge intensity
    
    return {
        'skin_brightness': skin_brightness / 3,  # Average RGB
        'skin_saturation': skin_saturation,
        'skin_smoothness': skin_smoothness,
        'overall_skin_health': calculate_skin_health_score(skin_brightness/3, skin_saturation, skin_smoothness)
    }

def analyze_facial_symmetry(image):
    """
    Analyze facial symmetry (basic implementation)
    """
    width, height = image.size
    
    # Split image into left and right halves
    left_half = image.crop((0, 0, width//2, height))
    right_half = image.crop((width//2, 0, width, height))
    
    # Flip right half to compare with left
    right_half_flipped = right_half.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Calculate statistical difference
    left_stats = ImageStat.Stat(left_half)
    right_stats = ImageStat.Stat(right_half_flipped)
    
    # Calculate symmetry score
    symmetry_diff = 0
    for i in range(3):  # RGB channels
        symmetry_diff += abs(left_stats.mean[i] - right_stats.mean[i])
    
    symmetry_score = max(0, 100 - symmetry_diff)
    
    return {
        'symmetry_score': symmetry_score,
        'asymmetry_level': symmetry_diff
    }

def analyze_facial_colors(image):
    """
    Analyze facial colors for health indicators
    """
    # Convert to different color spaces
    rgb_stats = ImageStat.Stat(image)
    hsv_image = image.convert('HSV')
    hsv_stats = ImageStat.Stat(hsv_image)
    
    # Calculate color health indicators
    red_level = rgb_stats.mean[0]
    green_level = rgb_stats.mean[1]
    blue_level = rgb_stats.mean[2]
    
    # Health indicators based on color balance
    color_balance = abs(red_level - green_level) + abs(green_level - blue_level) + abs(blue_level - red_level)
    
    # Pallor indicator (low red levels might indicate fatigue)
    pallor_indicator = max(0, 120 - red_level)
    
    return {
        'red_level': red_level,
        'green_level': green_level,
        'blue_level': blue_level,
        'color_balance': color_balance,
        'pallor_indicator': pallor_indicator,
        'overall_complexion_health': calculate_complexion_health(red_level, green_level, blue_level, color_balance)
    }

def analyze_image_brightness(image):
    """
    Analyze overall image brightness and lighting conditions
    """
    # Convert to grayscale for brightness analysis
    gray_image = image.convert('L')
    brightness_stats = ImageStat.Stat(gray_image)
    
    # Analyze lighting conditions
    brightness_mean = brightness_stats.mean[0]
    brightness_std = brightness_stats.stddev[0]
    
    # Determine lighting quality
    if brightness_mean < 50:
        lighting_quality = "Too Dark"
    elif brightness_mean > 200:
        lighting_quality = "Too Bright"
    elif brightness_std > 50:
        lighting_quality = "Uneven Lighting"
    else:
        lighting_quality = "Good Lighting"
    
    return {
        'brightness_level': brightness_mean,
        'brightness_variation': brightness_std,
        'lighting_quality': lighting_quality,
        'optimal_lighting': 80 <= brightness_mean <= 180 and brightness_std <= 40
    }

def calculate_fatigue_score(analysis_results):
    """
    Calculate overall fatigue score based on all analyses
    """
    score = 0
    
    # Eye analysis contribution (40%)
    eye_fatigue = analysis_results['eye_analysis']['fatigue_score']
    score += eye_fatigue * 0.4
    
    # Skin condition contribution (25%)
    skin_health = analysis_results['skin_analysis']['overall_skin_health']
    score += (100 - skin_health) * 0.25
    
    # Color analysis contribution (20%)
    complexion_health = analysis_results['color_analysis']['overall_complexion_health']
    score += (100 - complexion_health) * 0.2
    
    # Symmetry contribution (10%)
    symmetry_score = analysis_results['facial_symmetry']['symmetry_score']
    score += (100 - symmetry_score) * 0.1
    
    # Lighting adjustment (5%)
    if not analysis_results['brightness_analysis']['optimal_lighting']:
        score += 5
    
    return min(100, max(0, score))

def calculate_eye_fatigue_score(brightness, dark_circles, puffiness):
    """
    Calculate eye-specific fatigue score
    """
    score = 0
    
    # Dark circles contribute to fatigue
    if dark_circles > 20:
        score += 30
    elif dark_circles > 10:
        score += 15
    
    # Low brightness indicates tired eyes
    if brightness < 80:
        score += 25
    elif brightness < 100:
        score += 10
    
    # High puffiness indicates fatigue
    if puffiness > 30:
        score += 25
    elif puffiness > 20:
        score += 15
    
    return min(100, score)

def calculate_skin_health_score(brightness, saturation, smoothness):
    """
    Calculate skin health score
    """
    score = 100
    
    # Optimal brightness range
    if brightness < 80 or brightness > 180:
        score -= 20
    
    # Saturation should be moderate
    if saturation < 20 or saturation > 80:
        score -= 15
    
    # Smoothness indicates healthy skin
    if smoothness < 200:
        score -= 25
    
    return max(0, score)

def calculate_complexion_health(red, green, blue, balance):
    """
    Calculate complexion health score
    """
    score = 100
    
    # Check for healthy color balance
    if balance > 50:
        score -= 30
    elif balance > 30:
        score -= 15
    
    # Check for pallor (low red levels)
    if red < 100:
        score -= 25
    
    # Check for overall color levels
    avg_color = (red + green + blue) / 3
    if avg_color < 80 or avg_color > 200:
        score -= 20
    
    return max(0, score)

def determine_sleep_indicators(analysis_results):
    """
    Determine specific sleep quality indicators from face analysis
    """
    indicators = {}
    
    fatigue_score = analysis_results['overall_fatigue_score']
    eye_analysis = analysis_results['eye_analysis']
    skin_analysis = analysis_results['skin_analysis']
    
    # Sleep deprivation indicators
    if fatigue_score > 70:
        indicators['sleep_deprivation'] = 'High'
    elif fatigue_score > 40:
        indicators['sleep_deprivation'] = 'Moderate'
    else:
        indicators['sleep_deprivation'] = 'Low'
    
    # Dark circles
    if eye_analysis['dark_circle_intensity'] > 20:
        indicators['dark_circles'] = 'Prominent'
    elif eye_analysis['dark_circle_intensity'] > 10:
        indicators['dark_circles'] = 'Mild'
    else:
        indicators['dark_circles'] = 'Minimal'
    
    # Eye puffiness
    if eye_analysis['puffiness_indicator'] > 30:
        indicators['eye_puffiness'] = 'High'
    elif eye_analysis['puffiness_indicator'] > 20:
        indicators['eye_puffiness'] = 'Moderate'
    else:
        indicators['eye_puffiness'] = 'Low'
    
    # Skin condition
    if skin_analysis['overall_skin_health'] > 80:
        indicators['skin_condition'] = 'Healthy'
    elif skin_analysis['overall_skin_health'] > 60:
        indicators['skin_condition'] = 'Fair'
    else:
        indicators['skin_condition'] = 'Poor'
    
    return indicators

def generate_face_recommendations(analysis_results, user_info):
    """
    Generate personalized recommendations based on face analysis
    """
    recommendations = []
    
    fatigue_score = analysis_results['overall_fatigue_score']
    eye_analysis = analysis_results['eye_analysis']
    skin_analysis = analysis_results['skin_analysis']
    brightness_analysis = analysis_results['brightness_analysis']
    
    # High fatigue recommendations
    if fatigue_score > 60:
        recommendations.extend([
            "Your face shows signs of significant fatigue. Prioritize getting 7-9 hours of quality sleep.",
            "Consider taking short power naps (20-30 minutes) if you're sleep deprived.",
            "Reduce screen time 1-2 hours before bedtime to improve sleep quality."
        ])
    
    # Dark circles recommendations
    if eye_analysis['dark_circle_intensity'] > 15:
        recommendations.extend([
            "Dark circles detected. Ensure adequate sleep and consider using a cold compress in the morning.",
            "Stay hydrated and consider using an eye cream with caffeine or vitamin C.",
            "Elevate your head while sleeping to reduce fluid accumulation under eyes."
        ])
    
    # Puffiness recommendations
    if eye_analysis['puffiness_indicator'] > 25:
        recommendations.extend([
            "Eye puffiness detected. Try sleeping with your head slightly elevated.",
            "Apply cold compresses or chilled cucumber slices to reduce swelling.",
            "Reduce salt intake, especially in the evening, to minimize fluid retention."
        ])
    
    # Skin condition recommendations
    if skin_analysis['overall_skin_health'] < 70:
        recommendations.extend([
            "Your skin shows signs of fatigue. Maintain a consistent skincare routine.",
            "Stay hydrated by drinking plenty of water throughout the day.",
            "Consider using a moisturizer with hyaluronic acid to improve skin appearance."
        ])
    
    # Lighting recommendations
    if not brightness_analysis['optimal_lighting']:
        recommendations.append("For better analysis results, take photos in natural daylight or well-lit conditions.")
    
    # General recommendations
    if fatigue_score > 30:
        recommendations.extend([
            "Regular exercise can improve sleep quality and reduce facial signs of fatigue.",
            "Practice stress management techniques like meditation or deep breathing.",
            "Maintain a consistent sleep schedule, even on weekends."
        ])
    
    return recommendations

def generate_face_insights(analysis_results):
    """
    Generate detailed insights from face analysis
    """
    insights = []
    
    fatigue_score = analysis_results['overall_fatigue_score']
    eye_analysis = analysis_results['eye_analysis']
    skin_analysis = analysis_results['skin_analysis']
    color_analysis = analysis_results['color_analysis']
    
    # Overall fatigue insight
    if fatigue_score > 70:
        insights.append("Your facial analysis indicates high levels of fatigue, which may be affecting your appearance and overall well-being.")
    elif fatigue_score > 40:
        insights.append("Moderate signs of fatigue are visible in your facial features, suggesting room for improvement in sleep quality.")
    else:
        insights.append("Your face shows minimal signs of fatigue, indicating good sleep habits and overall health.")
    
    # Eye-specific insights
    if eye_analysis['dark_circle_intensity'] > 20:
        insights.append("Prominent dark circles may indicate chronic sleep deprivation, dehydration, or genetic predisposition.")
    
    if eye_analysis['puffiness_indicator'] > 30:
        insights.append("Eye puffiness can result from fluid retention, often caused by poor sleep position, high sodium intake, or inadequate sleep.")
    
    # Skin insights
    if skin_analysis['skin_smoothness'] < 180:
        insights.append("Skin texture analysis suggests potential dehydration or fatigue affecting your complexion.")
    
    # Color insights
    if color_analysis['pallor_indicator'] > 30:
        insights.append("Facial pallor detected, which can be associated with fatigue, poor circulation, or inadequate rest.")
    
    # Positive insights
    if fatigue_score < 30:
        insights.append("Your facial analysis shows good signs of rest and recovery, indicating effective sleep habits.")
    
    return insights

def sleep_need_from_face(fatigue_score, age):
    """
    Recommend sleep duration based on face analysis and age
    """
    # Base sleep recommendations by age
    if age <= 25:
        base_sleep = 8
    elif age <= 40:
        base_sleep = 7.5
    else:
        base_sleep = 7
    
    # Adjust based on fatigue score
    if fatigue_score > 70:
        base_sleep += 1.5  # Significant additional sleep needed
    elif fatigue_score > 50:
        base_sleep += 1    # Moderate additional sleep needed
    elif fatigue_score > 30:
        base_sleep += 0.5  # Slight additional sleep needed
    
    return min(base_sleep, 10)  # Cap at 10 hours

def analyze_face(eye_closed_frames=0):
    """
    Legacy function for backward compatibility
    """
    if eye_closed_frames > 20:
        fatigue_score = 80   # High fatigue
    elif eye_closed_frames > 10:
        fatigue_score = 50   # Moderate fatigue
    else:
        fatigue_score = 20   # Normal

    return fatigue_score
