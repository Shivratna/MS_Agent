import json
from typing import List
from models import StudentProfile, Program, QNAPair
from utils.gemini_client import GeminiClient

class QNAGeneratorAgent:
    """Generates curated Q&A pairs based on student profile and shortlisted programs"""
    
    def __init__(self, client: GeminiClient):
        self.client = client
    
    def generate_questions(self, profile: StudentProfile, programs: List[Program]) -> List[QNAPair]:
        """
        Generates exactly 5 relevant Q&A pairs for the student's journey.
        Single API call - safe for free tier.
        """
        # Extract key info
        countries = list(set([p.country for p in programs[:3]]))  # Top 3 countries
        program_names = [p.name for p in programs[:2]]  # Top 2 programs
        
        prompt = f"""
        You are an expert MS application advisor. Generate EXACTLY 5 most relevant Q&A pairs 
        for a student at this stage of their application journey.
        
        **Student Context:**
        - Target Degree: {profile.target_degree}
        - Target Countries: {countries}
        - Top Programs: {program_names}
        - GPA: {profile.gpa}
        - Test Scores: {profile.test_scores if profile.test_scores else 'Not provided'}
        - Budget: {profile.budget}
        
        **Generate 5 Q&A pairs following these rules:**
        
        1. **Questions**: 
           - Maximum 30 characters each
           - Highly specific to their situation (countries, programs, tests)
           - Actionable and commonly asked
           - Examples: "What is APS for Germany?", "Do I need GRE?", "Blocked account amount?"
        
        2. **Answers**: 
           - Maximum 30 words each
           - Student-friendly, no jargon
           - Factual and helpful
           - End with "Source: General knowledge"
        
        3. **Categories**: 
           - Use one of: "country", "tests", "documents", "visa", "sop", "general"
        
        4. **Prioritize**:
           - Country-specific requirements (e.g., APS for Germany, blocked account)
           - Test requirements (GRE/TOEFL based on their scores)
           - Application documents (SOP, LOR timing)
           - Visa process timing
           - Common pitfalls
        
        **Return ONLY valid JSON in this exact format (no markdown, no extra text):**
        {{
          "qna_pairs": [
            {{"question": "What is APS certificate?", "answer": "APS is mandatory for Indians applying to Germany. Verify documents at APS center. Costs ~₹18k, takes 2-3 months. Source: General knowledge", "category": "country"}},
            {{"question": "Blocked account amount?", "answer": "Need €11,904/year in blocked account for German student visa. Open via Fintiba or Deutsche Bank. Source: General knowledge", "category": "visa"}},
            {{"question": "GRE needed for Germany?", "answer": "Most German MS programs don't require GRE. Check specific program requirements on university website. Source: General knowledge", "category": "tests"}},
            {{"question": "When to start SOP?", "answer": "Start SOP 4-6 weeks before deadline. Highlight research interests and career goals. Get 2-3 peer reviews. Source: General knowledge", "category": "sop"}},
            {{"question": "Visa process timeline?", "answer": "Start visa 3 months before program starts. Need admission letter, blocked account, health insurance first. Source: General knowledge", "category": "visa"}}
          ]
        }}
        
        **Important**: Generate questions relevant to {countries} and the degree {profile.target_degree}. Return ONLY the JSON object, nothing else.
        """
        
        try:
            # Use GeminiClient's generate_content method without schema
            response_text = self.client.generate_content(prompt=prompt).strip()
            
            # Clean response (remove markdown code blocks if present)
            if response_text.startswith('```'):
                # Extract JSON from markdown code block
                lines = response_text.split('\n')
                response_text = '\n'.join([line for line in lines if not line.startswith('```')])
                response_text = response_text.strip()
            
            data = json.loads(response_text)
            
            qna_pairs = []
            for item in data.get('qna_pairs', [])[:5]:  # Ensure exactly 5
                qna_pairs.append(QNAPair(
                    question=item.get('question', '')[:30],  # Enforce 30 char limit
                    answer=item.get('answer', ''),
                    category=item.get('category', 'general')
                ))
            
            # If less than 5, add generic fallback
            while len(qna_pairs) < 5:
                qna_pairs.append(QNAPair(
                    question="Application tips?",
                    answer="Start early, get strong LORs, tailor SOP to each program. Review deadlines weekly. Source: General knowledge",
                    category="general"
                ))
            
            return qna_pairs[:5]  # Return exactly 5
            
        except Exception as e:
            print(f"Error in QNAGeneratorAgent: {e}")
            # Return safe fallback questions
            return [
                QNAPair(
                    question="When to start applying?",
                    answer="Start 6-8 months before deadline. Research programs, prepare documents, draft SOP early. Source: General knowledge",
                    category="general"
                ),
                QNAPair(
                    question="Strong SOP tips?",
                    answer="Highlight research interests, career goals, and why this program. Be specific and authentic. Source: General knowledge",
                    category="sop"
                ),
                QNAPair(
                    question="LOR best practices?",
                    answer="Request from professors who know you well. Give 4-6 weeks notice. Provide resume and project details. Source: General knowledge",
                    category="documents"
                ),
                QNAPair(
                    question="Test scores needed?",
                    answer="Check each program's requirements. GRE often optional, TOEFL/IELTS for non-native English speakers. Source: General knowledge",
                    category="tests"
                ),
                QNAPair(
                    question="Application checklist?",
                    answer="Transcripts, SOP, LORs, test scores, CV, application fee. Verify program-specific requirements. Source: General knowledge",
                    category="documents"
                )
            ]
