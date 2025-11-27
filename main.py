import os
import json
import dataclasses
from orchestrator import Orchestrator

# Helper to serialize dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def main():
    # Sample Input
    sample_student = {
        "gpa": 3.6,
        "degree": "Masters in Computer Science",
        "countries": ["Germany", "USA"],
        "budget": "Medium",
        "interests": ["Artificial Intelligence", "Machine Learning"],
        "intake": "Fall 2025",
        "tests": {
            "GRE": "320",
            "TOEFL": "105"
        }
    }

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    orchestrator = Orchestrator()
    results = orchestrator.run(sample_student)

    # Pretty Print Results
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    
    print(json.dumps(results, cls=EnhancedJSONEncoder, indent=2))

    # Save to file
    with open("output.json", "w") as f:
        json.dump(results, f, cls=EnhancedJSONEncoder, indent=2)
    print("\nResults saved to output.json")

if __name__ == "__main__":
    main()
