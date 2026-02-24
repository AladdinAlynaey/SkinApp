"""
Diagnosis Pipeline - Multi-stage AI processing

Orchestrates the 5-stage diagnosis pipeline with fallback handling.
"""

import time
from typing import Dict, Optional
from dataclasses import dataclass, field
from storage import DiagnosisStore
from storage.log_store import LogStore
from utils.logger import get_logger
from .router import AIRouter

logger = get_logger('pipeline')


@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    stage0: Dict = field(default_factory=dict)
    stage1: Dict = field(default_factory=dict)
    stage2: Dict = field(default_factory=dict)
    stage3: Dict = field(default_factory=dict)
    stage4: Dict = field(default_factory=dict)
    error: Optional[str] = None
    total_duration_ms: int = 0


class DiagnosisPipeline:
    """
    Multi-stage AI diagnosis pipeline.
    
    Stage 0: Validation Gate (MANDATORY) - Is this valid skin/medical image?
    Stage 1: Normal vs Abnormal classification
    Stage 2: Disease category classification  
    Stage 3: Fine-grained disease diagnosis
    Stage 4: AI Fusion - Combine all data for final diagnosis
    """
    
    def __init__(self):
        self.router = AIRouter()
        self.diagnosis_store = DiagnosisStore()
        self.log_store = LogStore()
    
    def execute(self, diagnosis_id: str, image_path: str, 
                image_bytes: bytes, patient_data: Dict) -> Dict:
        """
        Execute the full diagnosis pipeline.
        
        CRITICAL: Stage 0 MUST pass or entire pipeline is rejected.
        """
        start_time = time.time()
        result = PipelineResult(success=False)
        
        try:
            # ========== STAGE 0: MANDATORY GATE ==========
            logger.info(f"[{diagnosis_id}] Stage 0: Validation Gate")
            
            stage0_result = self._execute_stage0(
                diagnosis_id, image_path, image_bytes
            )
            result.stage0 = stage0_result
            
            self.diagnosis_store.update_pipeline_stage(
                diagnosis_id, 'stage0', stage0_result
            )
            
            # STAGE 0 MUST PASS - NO EXCEPTIONS
            if not stage0_result.get('is_valid'):
                result.error = stage0_result.get('rejection_reason', 
                    'Image validation failed')
                logger.warning(f"[{diagnosis_id}] Stage 0 REJECTED: {result.error}")
                return self._finalize_result(result, start_time)
            
            # ========== STAGE 1: NORMAL VS ABNORMAL ==========
            logger.info(f"[{diagnosis_id}] Stage 1: Normal/Abnormal Classification")
            
            stage1_result = self._execute_stage1(
                diagnosis_id, image_path, image_bytes
            )
            result.stage1 = stage1_result
            
            self.diagnosis_store.update_pipeline_stage(
                diagnosis_id, 'stage1', stage1_result
            )
            
            # If normal, skip to Stage 4
            if stage1_result.get('classification') == 'normal':
                logger.info(f"[{diagnosis_id}] Classified as normal, skipping to fusion")
                result.stage2 = {'skipped': True, 'reason': 'normal_classification'}
                result.stage3 = {'skipped': True, 'reason': 'normal_classification'}
            else:
                # ========== STAGE 2: CATEGORY CLASSIFICATION ==========
                logger.info(f"[{diagnosis_id}] Stage 2: Category Classification")
                
                stage2_result = self._execute_stage2(
                    diagnosis_id, image_path, image_bytes, stage1_result
                )
                result.stage2 = stage2_result
                
                self.diagnosis_store.update_pipeline_stage(
                    diagnosis_id, 'stage2', stage2_result
                )
                
                # ========== STAGE 3: FINE-GRAINED DIAGNOSIS ==========
                logger.info(f"[{diagnosis_id}] Stage 3: Disease Diagnosis")
                
                stage3_result = self._execute_stage3(
                    diagnosis_id, image_path, image_bytes, 
                    stage1_result, stage2_result
                )
                result.stage3 = stage3_result
                
                self.diagnosis_store.update_pipeline_stage(
                    diagnosis_id, 'stage3', stage3_result
                )
            
            # ========== STAGE 4: AI FUSION ==========
            logger.info(f"[{diagnosis_id}] Stage 4: AI Fusion")
            
            stage4_result = self._execute_stage4(
                diagnosis_id, patient_data, result
            )
            result.stage4 = stage4_result
            
            self.diagnosis_store.update_pipeline_stage(
                diagnosis_id, 'stage4', stage4_result
            )
            
            result.success = True
            logger.info(f"[{diagnosis_id}] Pipeline completed successfully")
            
        except Exception as e:
            logger.exception(f"[{diagnosis_id}] Pipeline error")
            result.error = str(e)
        
        return self._finalize_result(result, start_time)
    
    def _execute_stage0(self, diagnosis_id: str, image_path: str, 
                        image_bytes: bytes) -> Dict:
        """Stage 0: Validate image is usable medical skin image."""
        from .stage0_gate import Stage0Gate
        
        gate = Stage0Gate(self.router)
        return gate.validate(diagnosis_id, image_path, image_bytes)
    
    def _execute_stage1(self, diagnosis_id: str, image_path: str,
                        image_bytes: bytes) -> Dict:
        """Stage 1: Normal vs Abnormal."""
        from .stage1_classifier import Stage1Classifier
        
        classifier = Stage1Classifier(self.router)
        return classifier.classify(diagnosis_id, image_path, image_bytes)
    
    def _execute_stage2(self, diagnosis_id: str, image_path: str,
                        image_bytes: bytes, stage1: Dict) -> Dict:
        """Stage 2: Disease category."""
        from .stage2_category import Stage2Category
        
        classifier = Stage2Category(self.router)
        return classifier.classify(diagnosis_id, image_path, image_bytes, stage1)
    
    def _execute_stage3(self, diagnosis_id: str, image_path: str,
                        image_bytes: bytes, stage1: Dict, stage2: Dict) -> Dict:
        """Stage 3: Fine-grained diagnosis."""
        from .stage3_diagnosis import Stage3Diagnosis
        
        diagnoser = Stage3Diagnosis(self.router)
        return diagnoser.diagnose(diagnosis_id, image_path, image_bytes, 
                                   stage1, stage2)
    
    def _execute_stage4(self, diagnosis_id: str, patient_data: Dict,
                        result: PipelineResult) -> Dict:
        """Stage 4: Fusion layer."""
        from .stage4_fusion import Stage4Fusion
        
        fusion = Stage4Fusion(self.router)
        return fusion.fuse(diagnosis_id, patient_data, 
                          result.stage1, result.stage2, result.stage3)
    
    def _finalize_result(self, result: PipelineResult, start_time: float) -> Dict:
        """Convert result to dictionary."""
        result.total_duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            'success': result.success,
            'stage0': result.stage0,
            'stage1': result.stage1,
            'stage2': result.stage2,
            'stage3': result.stage3,
            'stage4': result.stage4,
            'error': result.error,
            'total_duration_ms': result.total_duration_ms
        }
