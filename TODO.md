# Cleanup Unwanted Files - SentimentIQ

## Steps:
- [x] Plan approved by user (keep sample_data)
- [ ] Check for backend/venv and frontend/dist presence  
- [ ] Delete frontend/src/components/UI/index.js (redundant JS barrel export)
- [ ] Delete backend/models/event_new.py (duplicate of event.py)
- [ ] Remove backend/venv (regenerable with pip)
- [ ] Remove frontend/dist (vite build artifact)
- [ ] Verify no errors in imports/workflow
- [ ] Recreate environments and test
- [ ] Mark complete
