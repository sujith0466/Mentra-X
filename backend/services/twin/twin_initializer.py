import logging
from backend.models import db, StudentTwinRecord
from backend.services.twin.twin_builder import build_initial_twin

logger = logging.getLogger(__name__)

class TwinInitializationService:
    @staticmethod
    def ensure_twin(user_id: int, exam_track: str = "JEE") -> StudentTwinRecord:
        """
        Ensures a StudentTwinRecord exists for the given user_id.
        If it does not exist, builds and returns a new Twin.
        Records initialization events.
        """
        try:
            twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).first()
            if twin:
                return twin

            logger.info(f"TwinInitializationStarted: user_id={user_id}")
            
            # Build the full twin (which creates it in the database)
            built_twin = build_initial_twin(user_id, exam_track)
            
            logger.info(f"TwinInitialized: user_id={user_id}, twin_id={built_twin.id}")
            return built_twin
            
        except Exception as e:
            logger.error(f"TwinInitializationError: user_id={user_id} error={str(e)}")
            raise e
