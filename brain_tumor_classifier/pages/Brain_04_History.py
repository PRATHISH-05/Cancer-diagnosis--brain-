"""
History Page - View past detections with detailed exports
"""
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Detection History", page_icon="📋", layout="wide")

st.markdown("""
<style>
    .history-header {
        font-size: 2.5rem;
        color: #1f77b4;
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

st.markdown('<h1 class="history-header">📋 Brain Tumor Detection History</h1>', unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("pages/Brain_01_Dashboard.py")

HISTORY_FILE = "detection_history.json"
TUMOR_COLORS = {'Glioma': '#FF6B6B', 'Meningioma': '#FFA500', 'No Tumor': '#51CF66', 'Pituitary': '#A78BFA'}

def load_history():
    """Load detection history"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def clear_history():
    """Clear detection history"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.success("✅ History cleared!")
    st.rerun()

history = load_history()

if not history:
    st.info("📭 No detection history yet. Upload and test images to see results here!")
else:
    # Statistics
    st.subheader("📊 Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tests", len(history))
    
    with col2:
        tumor_types = {}
        for entry in history:
            t_type = entry['tumor_type']
            tumor_types[t_type] = tumor_types.get(t_type, 0) + 1
        st.metric("Tumor Types Found", len(tumor_types))
    
    with col3:
        avg_confidence = sum([e['confidence'] for e in history]) / len(history) if history else 0
        st.metric("Avg Confidence", f"{avg_confidence:.2f}%")
    
    with col4:
        no_tumor_count = sum([1 for e in history if e['tumor_type'] == 'No Tumor'])
        st.metric("No Tumor Cases", no_tumor_count)
    
    # Breakdown chart
    st.markdown("---")
    st.subheader("📈 Tumor Type Breakdown")
    
    tumor_types = {}
    for entry in history:
        t_type = entry['tumor_type']
        tumor_types[t_type] = tumor_types.get(t_type, 0) + 1
    
    if tumor_types:
        chart_df = pd.DataFrame({'Tumor Type': list(tumor_types.keys()), 'Count': list(tumor_types.values())})
        st.bar_chart(chart_df.set_index('Tumor Type'))
    
    # Detailed history table
    st.markdown("---")
    st.subheader("🔍 Detailed History")
    
    history_sorted = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    # Enhanced DataFrame
    df_display = []
    for entry in history_sorted:
        df_display.append({
            'Date': entry['timestamp'],
            'Image': entry['image'],
            'Tumor Type': entry['tumor_type'],
            'Confidence %': entry['confidence'],
            'Glioma %': entry.get('Glioma%', 'N/A'),
            'Meningioma %': entry.get('Meningioma%', 'N/A'),
            'No Tumor %': entry.get('No Tumor%', 'N/A'),
            'Pituitary %': entry.get('Pituitary%', 'N/A'),
        })
    
    df = pd.DataFrame(df_display)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Individual entries with full details
    st.markdown("---")
    st.subheader("📝 Individual Detections")
    
    for idx, entry in enumerate(history_sorted[:5]):
        tumor_type = entry['tumor_type']
        color = TUMOR_COLORS.get(tumor_type, '#1f77b4')
        
        st.markdown(f"""
        <div class="history-card" style="border-left-color: {color};">
            <b style="color: #000;">Test #{len(history) - idx}</b><br/>
            <span class="history-text">📸 <b>File:</b> {entry['image']}</span><br/>
            <span class="history-text">🎯 <b>Detection:</b> <span style="color: {color}; font-weight: bold;">{tumor_type}</span></span><br/>
            <span class="history-text">📊 <b>Confidence:</b> {entry['confidence']}%</span><br/>
            <span class="history-text">🧬 <b>Predictions:</b> Glioma: {entry.get('Glioma%', 'N/A')}% | Meningioma: {entry.get('Meningioma%', 'N/A')}% | No Tumor: {entry.get('No Tumor%', 'N/A')}% | Pituitary: {entry.get('Pituitary%', 'N/A')}%</span><br/>
            <span class="history-text">🕐 <b>Date:</b> {entry['timestamp']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if len(history_sorted) > 5:
        st.info(f"... and {len(history_sorted) - 5} more detections")
    
    # Export options
    st.markdown("---")
    st.subheader("⬇️ Export History")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Enhanced CSV export with all predictions
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Detailed CSV",
            data=csv_data,
            file_name=f"brain_history_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="csv_export"
        )
    
    with col2:
        # JSON export
        json_data = json.dumps(history_sorted, indent=4)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"brain_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="json_export"
        )
    
    with col3:
        # Summary export
        summary_text = f"Brain Tumor Detection Summary Report\n{'='*50}\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        summary_text += f"STATISTICS:\n- Total Tests: {len(history)}\n- Average Confidence: {avg_confidence:.2f}%\n- Tumor Types Found: {len(tumor_types)}\n"
        summary_text += f"- No Tumor Cases: {no_tumor_count}\n\n"
        summary_text += f"TUMOR TYPE DISTRIBUTION:\n"
        for tumor_type, count in tumor_types.items():
            percentage = (count / len(history)) * 100
            summary_text += f"- {tumor_type}: {count} ({percentage:.1f}%)\n"
        
        summary_text += f"\n{'='*50}\nDETAILED RECORDS:\n"
        for idx, entry in enumerate(history_sorted, 1):
            summary_text += f"\nTest #{idx}\n"
            summary_text += f"  Date: {entry['timestamp']}\n"
            summary_text += f"  Image: {entry['image']}\n"
            summary_text += f"  Result: {entry['tumor_type']}\n"
            summary_text += f"  Confidence: {entry['confidence']}%\n"
            summary_text += f"  All Predictions: Glioma={entry.get('Glioma%', 'N/A')}%, Meningioma={entry.get('Meningioma%', 'N/A')}%, No Tumor={entry.get('No Tumor%', 'N/A')}%, Pituitary={entry.get('Pituitary%', 'N/A')}%\n"
        
        st.download_button(
            label="📋 Download Summary Report",
            data=summary_text,
            file_name=f"brain_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="summary_export"
        )
    
    # Clear history button
    st.markdown("---")
    if st.button("🗑️ Clear All History", help="This will delete all detection records"):
        clear_history()

# Footer Navigation
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back", key="footer_back"):
        st.switch_page("pages/Brain_01_Dashboard.py")

with footer_col2:
    if st.button("📚 Medical Info", key="footer_medical"):
        st.switch_page("pages/Brain_02_Medical_Info.py")

with footer_col3:
    if st.button("🔬 Test & Detect", key="footer_detect"):
        st.switch_page("pages/Brain_03_Test_Detect.py")

with footer_col4:
    if st.button("🏥 Home", key="footer_home"):
        st.switch_page("Home.py")
