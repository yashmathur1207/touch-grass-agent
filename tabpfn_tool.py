import os
import pandas as pd
import numpy as np
import warnings
from tabpfn_client import TabPFNClassifier 

# Suppress warnings for clean terminal output
warnings.filterwarnings("ignore", category=UserWarning)

class FatigueClassifier:
    def __init__(self):
        self.clf = TabPFNClassifier()
        self.features = [
            'session_duration_mins', 
            'keystrokes_per_min', 
            'error_rate_pct', 
            'time_since_last_break_mins'
        ]
        
        self.df = self._generate_synthetic_baseline()
        self.X_train = self.df[self.features]
        self.y_train = self.df['burnout_state']
        
        # Resilient Cloud Connection
        self.api_online = False
        try:
            print("[TabPFN] Attempting cloud connection...")
            self.clf.fit(self.X_train, self.y_train)
            self.api_online = True
            print("[TabPFN] Cloud model fitted successfully.")
        except Exception as e:
            print(f"[TabPFN Error]: Offline or key invalid. Details: {e}")
            print("[TabPFN] Falling back to heuristic mode.")

    def predict_burnout(self, current_session: dict) -> float:
        """Takes real-time session telemetry and returns a probability score."""
        try:
            # Attempt to use the cloud model
            X_new = pd.DataFrame([current_session])[self.features]
            probabilities = self.clf.predict_proba(X_new)
            burnout_probability = probabilities[0][1] 
            return round(float(burnout_probability), 4)
        except Exception as e:
            # If the model isn't fitted (API was down during startup) or fails here, use the fallback
            print(f"[TabPFN Fallback Triggered]: {e}")
            
            # Simple heuristic mock logic based on the payload you just sent
            if current_session.get('error_rate_pct', 0) > 0.10:
                return 0.88  # High burnout risk
            return 0.15      # Healthy state

    def _generate_synthetic_baseline(self) -> pd.DataFrame:
        """Generates 200 rows of mock telemetry to simulate past coding sessions."""
        np.random.seed(42)
        data = []
        for _ in range(200):
            if np.random.rand() > 0.5:
                data.append({
                    'session_duration_mins': np.random.randint(15, 60),
                    'keystrokes_per_min': np.random.randint(40, 90),
                    'error_rate_pct': round(np.random.uniform(0.01, 0.05), 3),
                    'time_since_last_break_mins': np.random.randint(5, 30),
                    'burnout_state': 0
                })
            else:
                data.append({
                    'session_duration_mins': np.random.randint(90, 300),
                    'keystrokes_per_min': np.random.randint(10, 50),
                    'error_rate_pct': round(np.random.uniform(0.08, 0.25), 3),
                    'time_since_last_break_mins': np.random.randint(90, 300),
                    'burnout_state': 1
                })
        return pd.DataFrame(data)