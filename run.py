#!/usr/bin/env python3
"""
Entry point for LeetCode Help Buddy development server.

Run with: python run.py
"""

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
