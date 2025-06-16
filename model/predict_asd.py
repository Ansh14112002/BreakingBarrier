def analyze_responses(responses):
    if not responses or len(responses) != 20:
        raise ValueError("Expected 20 responses")

    # Category mapping (0-indexed question positions)
    categories = {
        'Social Skills': [0, 1, 3, 7, 10, 12, 19],
        'Behavioral': [2, 6, 13, 15, 16, 17],
        'Sensory': [4, 8, 14],
        'Cognitive/Language': [5, 9, 11, 18]
    }

    # Compute raw total score
    total_score = sum(responses)
    max_score = 20 * 5  # assuming 5-point scale (1 to 5)
    percentage = round((total_score / max_score) * 100, 2)

    # Determine verdict
    if percentage < 40:
        verdict = "Low ASD Likelihood"
        advice = "Your responses indicate a low likelihood of Autism Spectrum Disorder. However, regular developmental screenings are recommended."
    elif percentage < 70:
        verdict = "Moderate ASD Likelihood"
        advice = "The responses show moderate traits. A formal assessment by a psychologist or pediatrician is advisable."
    else:
        verdict = "High ASD Likelihood"
        advice = "High likelihood of ASD based on your answers. Please consult a specialist for a professional diagnosis."

    # Category-wise scores
    category_scores = {}
    for category, indexes in categories.items():
        cat_total = sum(responses[i] for i in indexes)
        cat_max = len(indexes) * 5
        category_scores[category] = round((cat_total / cat_max) * 100, 2)

    return {
        'score': percentage,
        'verdict': verdict,
        'advice': advice,
        'category_scores': category_scores
    }
