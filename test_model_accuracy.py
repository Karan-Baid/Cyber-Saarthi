#!/usr/bin/env python3
"""
Test script to evaluate the fine-tuned Cyber Saarthi model's accuracy
"""
import sys
sys.path.insert(0, '/home/karan/projects/cyber-saarthi')

from cyber_saarthi.inference import CyberSaarthiModel

# Ground truth test cases with expected answers
TEST_CASES = [
    {
        "query": "What is Section 66C of the IT Act?",
        "expected_keywords": ["identity theft", "fraudulent", "electronic signature", "password", "imprisonment", "three years", "one lakh"],
        "category": "Specific Section"
    },
    {
        "query": "What are the penalties for unauthorized access to computer systems?",
        "expected_keywords": ["Section 43", "damages", "compensation", "crore"],
        "category": "Penalties"
    },
    {
        "query": "What is cyber terrorism under Indian law?",
        "expected_keywords": ["Section 66F", "life imprisonment", "unity", "integrity", "security", "sovereignty"],
        "category": "Serious Offenses"
    },
    {
        "query": "Explain Section 43A about data protection",
        "expected_keywords": ["sensitive personal data", "body corporate", "compensation", "reasonable security"],
        "category": "Data Protection"
    },
    {
        "query": "What is the punishment for hacking?",
        "expected_keywords": ["Section 66", "three years", "five lakh", "computer resource"],
        "category": "Common Crimes"
    }
]

def evaluate_response(response, expected_keywords):
    """Check how many expected keywords are in the response"""
    response_lower = response.lower()
    matches = [kw for kw in expected_keywords if kw.lower() in response_lower]
    score = len(matches) / len(expected_keywords) * 100
    return score, matches

def main():
    print("=" * 80)
    print("CYBER SAARTHI MODEL EVALUATION")
    print("=" * 80)
    print("\nLoading model...")
    
    model = CyberSaarthiModel("./models/cyber-saarthi/final")
    
    print("\n" + "=" * 80)
    print("TESTING MODEL RESPONSES")
    print("=" * 80)
    
    total_score = 0
    results = []
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n[Test {i}/{len(TEST_CASES)}] Category: {test['category']}")
        print(f"Query: {test['query']}")
        print("-" * 80)
        
        response = model.generate(
            test['query'],
            max_new_tokens=256,
            temperature=0.7
        )
        
        # Extract just the answer part
        if "Below is an instruction" in response:
            # Try to get just the generated answer
            parts = response.split(test['query'])
            if len(parts) > 1:
                response = parts[-1].strip()
        
        print(f"Response: {response[:500]}...")  # First 500 chars
        
        score, matches = evaluate_response(response, test['expected_keywords'])
        total_score += score
        
        print(f"\nKeywords matched: {len(matches)}/{len(test['expected_keywords'])} ({score:.1f}%)")
        print(f"Matched: {', '.join(matches)}")
        print(f"Missing: {', '.join([k for k in test['expected_keywords'] if k.lower() not in [m.lower() for m in matches]])}")
        
        results.append({
            'query': test['query'],
            'category': test['category'],
            'score': score,
            'matches': matches
        })
        
        print("=" * 80)
    
    # Summary
    avg_score = total_score / len(TEST_CASES)
    print(f"\n{'='*80}")
    print(f"EVALUATION SUMMARY")
    print(f"{'='*80}")
    print(f"Overall Accuracy: {avg_score:.1f}%")
    print(f"\nBreakdown by Category:")
    for result in results:
        print(f"  {result['category']:20s}: {result['score']:5.1f}%")
    
    if avg_score >= 70:
        print(f"\n✅ PASS - Model performs adequately (>70%)")
    elif avg_score >= 50:
        print(f"\n⚠️  MARGINAL - Model needs more training (50-70%)")
    else:
        print(f"\n❌ FAIL - Model needs significant more training (<50%)")
    
    print(f"\n💡 Recommendation: ", end="")
    if avg_score < 60:
        print("Run FULL training (3 epochs) instead of test mode (1 epoch)")
    else:
        print("Model is working! Can improve with more epochs if needed")

if __name__ == "__main__":
    main()
