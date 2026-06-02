# app.py
import streamlit as st
import streamlit.components.v1 as components
import backend as bg

# Page layout configuration
st.set_page_config(page_title="GraphRAG Trip Planner", page_icon="🕸️", layout="wide")

# Title Header Configuration
st.title("🕸️ Production GraphRAG Knowledge Engine")
st.caption("Context-grounded multi-hop generation leveraging NetworkX Entity Graphs & DeepEval Audits")

# Create split layout workspace columns (Left side control panel, Right side output layout)
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Plan Your Journey")
    form_destination = st.text_input("Where do you want to go?", placeholder="e.g. Paris or Tokyo")
    form_days = st.text_input("Duration of trip (Days):", placeholder="e.g. 5")
    submit_btn = st.button("Generate Graph-Grounded Itinerary", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("""
    ### 🕸️ Graph Layer Specifications
    * **Graph Store**: Memory-Optimized `NetworkX` Directed Graph
    * **Retrieval Method**: Subgraph Neighborhood Entity Extraction
    * **Knowledge Capture**: Explicit Triplet Mappings
    * **Quality Auditor**: DeepEval Automated Evaluation Layer
    """)

with col_output:
    st.subheader("🗺️ Live Itinerary Stream")
    
    if submit_btn:
        # 1. Run Input Guardrail Checks (Layer 1 & Layer 2)
        with st.spinner("Running security validation check..."):
            passed, guardrail_result = bg.run_input_guardrails(form_destination, form_days)
            
        if not passed:
            st.error(guardrail_result)
        else:
            processed_days = guardrail_result  # Contains our validated clean string number
            st.success("✅ Security Guardrails Cleared. Semantic alignment clear.")
            
            # 2. Extract Document Context Matrix from the Knowledge Graph
            with st.spinner("Traversing Knowledge Graph relationships..."):
                retrieved_graph_context = bg.get_graph_context(form_destination)
                
            # 3. Render the Knowledge Graph Audit Panel (Data vs Interactive Chart)
            with st.expander("🔍 View Extracted Knowledge Graph Triplets", expanded=True):
                tab_data, tab_chart = st.tabs(["📄 Graph Tuple Data", "🕸️ Interactive Graph Chart"])
                
                with tab_data:
                    st.code(retrieved_graph_context, language="text")
                    
                with tab_chart:
                    st.markdown("#### Live Network Topology View")
                    # Dynamically pass the variable form_destination to render chart layout
                    graph_html_code = bg.generate_graph_html(form_destination)
                    
                    if graph_html_code:
                        components.html(graph_html_code, height=420, scrolling=False)
                    else:
                        st.info("Insufficient relational connection node limits discovered to draw topology canvas map layout.")
            
            # 4. Stream Generated Tokens in Real Time
            st.markdown("#### 📝 Curated Itinerary")
            itinerary_placeholder = st.empty()
            full_itinerary_text = ""
            
            # Consume the stream generator method from backend script natively
            token_stream = bg.generate_itinerary_stream(form_destination, processed_days, retrieved_graph_context)
            full_itinerary_text = itinerary_placeholder.write_stream(token_stream)
            
            st.divider()
            
            # 5. Perform Real-Time DeepEval Automated Auditing Framework
            st.subheader("📊 DeepEval Real-Time Backend Analytics")
            with st.spinner("Analyzing output compliance alignment metrics..."):
                eval_metrics = bg.run_deepeval_audit(form_destination, processed_days, full_itinerary_text)
                
            # Create a KPI metric row scorecard display view layout
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric(label="Answer Relevancy Score", value=f"{eval_metrics['score']:.4f}")
            with metric_col2:
                status_label = "🟢 PASSED" if eval_metrics['passed'] else "🔴 FAILED"
                st.metric(label="Evaluation Framework Status", value=status_label)
                
            st.markdown(f"**Auditor Reasoning/Feedback Logging:** *{eval_metrics['reason']}*")