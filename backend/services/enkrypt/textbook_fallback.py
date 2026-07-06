"""
Mentra X — Enkrypt Textbook Fallback Service (Phase 7 Layer 6)

Provides pre-verified, human-authored textbook reference content (e.g., NCERT, Standard Reference)
for concepts when AI tutor responses undergo hard failures or double regeneration failures.
"""

from typing import Dict, Any, Optional
from backend.services.enkrypt.dto import FallbackContentDTO


class TextbookFallbackService:
    # In-memory seeded textbook content for JEE, NEET, UPSC, and CAT
    SEEDED_FALLBACKS: Dict[str, Dict[str, Dict[str, Any]]] = {
        "JEE": {
            "thermodynamics": {
                "subject": "physics",
                "content_text": "The Second Law of Thermodynamics states that the total entropy of an isolated system can never decrease over time, and is constant if and only if all processes are reversible. For an isothermal reversible process, change in entropy is given by \u0394S = Q_rev / T. In irreversible processes, \u0394S > Q / T.",
                "source": "NCERT Physics Class XI, Chapter 12: Thermodynamics"
            },
            "newton_laws": {
                "subject": "physics",
                "content_text": "Newton's Second Law of Motion states that the rate of change of momentum of a body is directly proportional to the applied force and takes place in the direction in which the force acts: F = dp/dt = m*a (for constant mass).",
                "source": "NCERT Physics Class XI, Chapter 5: Laws of Motion"
            },
            "relativity": {
                "subject": "physics",
                "content_text": "Mass-Energy Equivalence: In special relativity, the total energy E of an object at rest is equal to its rest mass m multiplied by the speed of light c squared: E = m*c^2.",
                "source": "NCERT Physics Class XII, Chapter 11: Dual Nature of Radiation and Matter"
            }
        },
        "NEET": {
            "photosynthesis": {
                "subject": "biology",
                "content_text": "Photosynthesis is an enzyme-regulated anabolic process of biochemical synthesis of organic compounds (glucose) inside the chlorophyll-containing cells (chloroplasts) from carbon dioxide and water with the help of sunlight as a source of energy. Note: Mitochondria are involved in cellular respiration (ATP synthesis), not glucose synthesis.",
                "source": "NCERT Biology Class XI, Chapter 13: Photosynthesis in Higher Plants"
            },
            "atomic_structure": {
                "subject": "chemistry",
                "content_text": "An atom consists of a positively charged nucleus (protons and neutrons) surrounded by negatively charged electrons (-1.6 x 10^-19 C) occupying quantized atomic orbitals.",
                "source": "NCERT Chemistry Class XI, Chapter 2: Structure of Atom"
            }
        },
        "UPSC": {
            "article_370": {
                "subject": "polity",
                "content_text": "Article 370 of the Indian Constitution, adopted in 1949, granted special status to Jammu and Kashmir. In August 2019, the Government of India revoked the special status granted under Article 370 through the Constitution (Application to Jammu and Kashmir) Order, 2019.",
                "source": "Indian Polity by M. Laxmikanth, 6th Edition"
            }
        },
        "CAT": {
            "time_speed_distance": {
                "subject": "quantitative",
                "content_text": "Fundamental relation: Distance = Speed * Time. To convert speed from km/h to m/s, multiply by 5/18. To convert speed from m/s to km/h, multiply by 18/5.",
                "source": "Quantitative Aptitude for CAT by Arun Sharma"
            }
        }
    }

    def get_fallback(self, concept: str, exam_track: str = "JEE", subject: str = "general") -> FallbackContentDTO:
        """
        Retrieves pre-verified textbook fallback content for the requested concept and track.
        Returns a generic reference fallback if specific concept is not seeded.
        """
        track_data = self.SEEDED_FALLBACKS.get(exam_track.upper(), {})
        # Try exact match or partial match
        matched = None
        for key, entry in track_data.items():
            if key in concept.lower() or concept.lower() in key:
                matched = entry
                break

        if matched:
            return FallbackContentDTO(
                concept_tag=concept,
                exam_track=exam_track,
                subject=matched.get("subject", subject),
                content_text=matched["content_text"],
                source=matched["source"]
            )
        else:
            return FallbackContentDTO(
                concept_tag=concept,
                exam_track=exam_track,
                subject=subject,
                content_text=f"Standard Reference Content for {concept.title()}: Please refer to official curriculum chapters and verified textbook formulations for rigorous derivations and problem-solving steps.",
                source=f"Official {exam_track} Standard Reference Curriculum"
            )
