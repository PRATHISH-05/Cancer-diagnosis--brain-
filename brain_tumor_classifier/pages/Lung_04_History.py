"""
Lung Cancer Detection History Page - View past detections with detailed exports
"""
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lung Cancer History", page_icon="📋", layout="wide")

st.markdown("""
<style>
    .history-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .history-card {
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
        color: #000;
    }
    .history-text {
        color: #000;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="history-header">📋 Lung Cancer Detection History</h1>', unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("pages/Lung_01_Dashboard.py")

HISTORY_FILE = "lung_detection_history.json"
CLASS_COLORS = {'Normal': '#51CF66', 'Benign': '#FFA500', 'Malignant': '#FF6B6B'}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.success("✅ History cleared!")
    st.rerun()

history = load_history()

if not history:
    st.info("📭 No detection history yet. Upload and test CT scans to see results here!")
else:
    st.subheader("📊 Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tests", len(history))
    
    with col2:
        classifications = {}
        for entry in history:
            c_type = entry['classification']
            classifications[c_type] = classifications.get(c_type, 0) + 1
        st.metric("Classifications", len(classifications))
    
    with col3:
        avg_confidence = sum([e['confidence'] for e in history]) / len(history) if history else 0
        st.metric("Avg Confidence", f"{avg_confidence:.2f}%")
    
    with col4:
        malignant_count = sum([1 for e in history if e['classification'] == 'Malignant'])
        st.metric("Malignant Cases", malignant_count)
    
    st.markdown("---")
    st.subheader("📈 Classification Breakdown")
    
    classifications = {}
    for entry in history:
        c_type = entry['classification']
        classifications[c_type] = classifications.get(c_type, 0) + 1
    
    if classifications:
        chart_df = pd.DataFrame({'Classification': list(classifications.keys()), 'Count': list(classifications.values())})
        st.bar_chart(chart_df.set_index('Classification'))
    
    st.markdown("---")
    st.subheader("🔍 Detailed History")
    
    history_sorted = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    df_display = []
    for entry in history_sorted:
        df_display.append({
            'Date': entry['timestamp'],
            'Image': entry['image'],
            'Classification': entry['classification'],
            'Confidence %': entry['confidence'],
            'Normal %': entry.get('Normal%', 'N/A'),
            'Benign %': entry.get('Benign%', 'N/A'),
            'Malignant %': entry.get('Malignant%', 'N/A'),
        })
    
    df = pd.DataFrame(df_display)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📝 Individual Detections")
    
    for idx, entry in enumerate(history_sorted[:5]):
        classification = entry['classification']
        color = CLASS_COLORS.get(classification, '#FF6B6B')
        
        st.markdown(f"""
        <div class="history-card" style="border-left-color: {color};">
            <b style="color: #000;">Test #{len(history) - idx}</b><br/>
            <span class="history-text">📸 <b>File:</b> {entry['image']}</span><br/>
            <span class="history-text">🎯 <b>Classification:</b> <span style="color: {color}; font-weight: bold;">{classification}</span></span><br/>
            <span class="history-text">📊 <b>Confidence:</b> {entry['confidence']}%</span><br/>
            <span class="history-text">🫁 <b>Predictions:</b> Normal: {entry.get('Normal%', 'N/A')}% | Benign: {entry.get('Benign%', 'N/A')}% | Malignant: {entry.get('Malignant%', 'N/A')}%</span><br/>
            <span class="history-text">🕐 <b>Date:</b> {entry['timestamp']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if len(history_sorted) > 5:
        st.info(f"... and {len(history_sorted) - 5} more detections")
    
    st.markdown("---")
    st.subheader("⬇️ Export History")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Detailed CSV",
            data=csv_data,
            file_name=f"lung_history_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="csv_export"
        )
    
    with col2:
        json_data = json.dumps(history_sorted, indent=4)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"lung_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="json_export"
        )
    
    with col3:
        summary_text = f"Lung Cancer Detection Summary Report\n{'='*50}\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        summary_text += f"STATISTICS:\n- Total Tests: {len(history)}\n- Average Confidence: {avg_confidence:.2f}%\n- Classifications Found: {len(classifications)}\n"
        summary_text += f"- Malignant Cases: {malignant_count}\n\n"
        summary_text += f"CLASSIFICATION DISTRIBUTION:\n"
        for c_type, count in classifications.items():
            percentage = (count / len(history)) * 100
            summary_text += f"- {c_type}: {count} ({percentage:.1f}%)\n"
        
        summary_text += f"\n{'='*50}\nDETAILED RECORDS:\n"
        for idx, entry in enumerate(history_sorted, 1):
            summary_text += f"\nTest #{idx}\n"
            summary_text += f"  Date: {entry['timestamp']}\n"
            summary_text += f"  Image: {entry['image']}\n"
            summary_text += f"  Result: {entry['classification']}\n"
            summary_text += f"  Confidence: {entry['confidence']}%\n"
            summary_text += f"  All Predictions: Normal={entry.get('Normal%', 'N/A')}%, Benign={entry.get('Benign%', 'N/A')}%, Malignant={entry.get('Malignant%', 'N/A')}%\n"
        
        st.download_button(
            label="📋 Download Summary Report",
            data=summary_text,
            file_name=f"lung_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="summary_export"
        )
    
    st.markdown("---")
    if st.button("🗑️ Clear All History", help="This will delete all detection records"):
        clear_history()

st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back", key="footer_back"):
        st.switch_page("pages/Lung_01_Dashboard.py")

with footer_col2:
    if st.button("📚 Medical Info", key="footer_medical"):
        st.switch_page("pages/Lung_02_Medical_Info.py")

with footer_col3:
    if st.button("🔬 Test & Detect", key="footer_detect"):
        st.switch_page("pages/Lung_03_Test_Detect.py")

with footer_col4:
    if st.button("🏥 Home", key="footer_home"):
        st.switch_page("Home.py")
