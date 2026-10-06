import sys
import os
import streamlit as st


# ============================================================
# ADD SRC FOLDER TO PYTHON PATH
# ============================================================


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from information_extraction import extract_disaster_information

from classification import (
    classify_message,
    classify_priority
)

from summarization import (
    generate_summary
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Disaster NLP Intelligent System",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🌍 Disaster NLP Intelligent Information System"
)

st.markdown(
    """
    **Natural Language Processing–Based Intelligent System for
    Disaster-Related Information Extraction and Automated
    Situation Summarization from Multisource Text Data**
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("System Modules")

    st.write("✅ Disaster Information Extraction")
    st.write("✅ Named Entity Recognition")
    st.write("✅ Emergency Detection")
    st.write("✅ Disaster Classification")
    st.write("✅ Priority Classification")
    st.write("✅ BART Situation Summarization")

    st.divider()

    st.info(
        "SDG Goal 11 – Sustainable Cities and Communities"
    )


# ============================================================
# SAMPLE MESSAGE
# ============================================================

default_message = """
Severe flooding has affected several houses in Coimbatore.
Five people are trapped and residents urgently need food and
medical assistance. Rescue teams are requested immediately.

Heavy rainfall has caused water levels to rise rapidly in
several areas. Roads have been flooded and transportation
has been disrupted.

Local residents have requested emergency rescue operations.
Medical teams and food supplies are also required.

Authorities are monitoring the situation and evacuation
operations are being considered for severely affected areas.
"""


# ============================================================
# INPUT
# ============================================================

st.subheader("📝 Disaster Information Input")

message = st.text_area(
    "Enter disaster-related information:",
    value=default_message,
    height=250
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "🔍 Analyze Disaster Information",
    type="primary",
    use_container_width=True
)


# ============================================================
# PROCESS
# ============================================================

if analyze:

    if not message.strip():

        st.warning(
            "Please enter disaster-related information."
        )

    else:

        try:

            with st.spinner(
                "Analyzing disaster information..."
            ):

                # ------------------------------------------------
                # INFORMATION EXTRACTION
                # ------------------------------------------------

                extracted = extract_disaster_information(
                    message
                )

                # ------------------------------------------------
                # CLASSIFICATION
                # ------------------------------------------------

                classification = classify_message(
                    message
                )

                # ------------------------------------------------
                # PRIORITY
                # ------------------------------------------------

                priority = classify_priority(
                    message
                )

                # ------------------------------------------------
                # SUMMARY
                # ------------------------------------------------

                summary = generate_summary(
                    message
                )

            st.success(
                "Disaster information analysis completed!"
            )


            # ====================================================
            # TOP METRICS
            # ====================================================

            st.subheader("📊 Disaster Analysis")

            col1, col2, col3, col4 = st.columns(4)


            # ----------------------------------------------------
            # Disaster type
            # ----------------------------------------------------

            with col1:

                disaster_type = extracted.get(
                    "Disaster Type",
                    "Unknown"
                )

                st.metric(
                    "Disaster Type",
                    disaster_type
                )


            # ----------------------------------------------------
            # Location
            # ----------------------------------------------------

            with col2:

                locations = extracted.get(
                    "Location",
                    []
                )

                if isinstance(locations, list):
                    location_text = ", ".join(
                        map(str, locations)
                    )
                else:
                    location_text = str(locations)

                if not location_text:
                    location_text = "Unknown"

                st.metric(
                    "Location",
                    location_text
                )


            # ----------------------------------------------------
            # Category
            # ----------------------------------------------------

            with col3:

                st.metric(
                    "Category",
                    classification.get(
                        "category",
                        "Unknown"
                    )
                )


            # ----------------------------------------------------
            # Priority
            # ----------------------------------------------------

            with col4:

                st.metric(
                    "Priority",
                    priority
                )


            st.divider()


            # ====================================================
            # INFORMATION EXTRACTION
            # ====================================================

            st.subheader(
                "📌 Extracted Disaster Information"
            )

            col1, col2 = st.columns(2)


            # ----------------------------------------------------
            # LEFT COLUMN
            # ----------------------------------------------------

            with col1:

                st.write(
                    "**Disaster Type:**",
                    disaster_type
                )

                st.write(
                    "**Location:**",
                    location_text
                )

                st.write(
                    "**Date:**",
                    extracted.get(
                        "Date",
                        "Unknown"
                    )
                )

                st.write(
                    "**Organization:**",
                    extracted.get(
                        "Organization",
                        []
                    )
                )

                st.write(
                    "**Severity:**",
                    extracted.get(
                        "Severity",
                        "Unknown"
                    )
                )


            # ----------------------------------------------------
            # RIGHT COLUMN
            # ----------------------------------------------------

            with col2:

                st.write(
                    "**People Trapped:**",
                    extracted.get(
                        "People Trapped",
                        0
                    )
                )

                st.write(
                    "**People Injured:**",
                    extracted.get(
                        "People Injured",
                        0
                    )
                )

                st.write(
                    "**People Missing:**",
                    extracted.get(
                        "People Missing",
                        0
                    )
                )

                st.write(
                    "**Deaths:**",
                    extracted.get(
                        "Deaths",
                        0
                    )
                )


            st.divider()


            # ====================================================
            # EMERGENCY INFORMATION
            # ====================================================

            st.subheader(
                "🚨 Emergency Information"
            )

            emergency_col1, emergency_col2 = st.columns(2)


            # ----------------------------------------------------
            # Emergency Needs
            # ----------------------------------------------------

            with emergency_col1:

                st.write(
                    "**Emergency Needs:**"
                )

                needs = extracted.get(
                    "Emergency Needs",
                    []
                )

                if needs:

                    for need in needs:

                        st.write(
                            f"• {need}"
                        )

                else:

                    st.write(
                        "No emergency needs detected."
                    )


            # ----------------------------------------------------
            # Emergency Indicators
            # ----------------------------------------------------

            with emergency_col2:

                st.write(
                    "**Emergency Indicators:**"
                )

                signals = classification.get(
                    "signals",
                    []
                )

                if signals:

                    for signal in signals:

                        st.write(
                            f"• {signal}"
                        )

                else:

                    st.write(
                        "No emergency indicators detected."
                    )


            st.divider()


            # ====================================================
            # CLASSIFICATION RESULTS
            # ====================================================

            st.subheader(
                "🤖 AI Classification"
            )

            class_col1, class_col2, class_col3 = st.columns(3)


            # ----------------------------------------------------
            # Predicted Category
            # ----------------------------------------------------

            with class_col1:

                st.write(
                    "**Predicted Category**"
                )

                st.success(
                    classification.get(
                        "category",
                        "Unknown"
                    )
                )


            # ----------------------------------------------------
            # Confidence
            # ----------------------------------------------------

            with class_col2:

                confidence = classification.get(
                    "confidence",
                    0
                )

                # Handle confidence already expressed
                # as percentage
                if confidence <= 1:
                    confidence_percentage = confidence * 100
                else:
                    confidence_percentage = confidence

                st.write(
                    "**Confidence**"
                )

                st.progress(
                    min(
                        max(
                            confidence_percentage / 100,
                            0
                        ),
                        1
                    )
                )

                st.write(
                    f"{confidence_percentage:.2f}%"
                )


            # ----------------------------------------------------
            # Priority Level
            # ----------------------------------------------------

            with class_col3:

                st.write(
                    "**Priority Level**"
                )

                if priority == "High":

                    st.error(
                        "🔴 HIGH"
                    )

                elif priority == "Medium":

                    st.warning(
                        "🟠 MEDIUM"
                    )

                else:

                    st.info(
                        "🟢 LOW"
                    )


            st.divider()


            # ====================================================
            # GENERATED SUMMARY
            # ====================================================

            st.subheader(
                "📰 Automated Situation Summary"
            )

            st.info(
                summary
            )


            st.divider()


            # ====================================================
            # ORIGINAL MESSAGE
            # ====================================================

            with st.expander(
                "📄 View Original Disaster Message"
            ):

                st.write(
                    message
                )


        except Exception as e:

            st.error(
                "An error occurred while analyzing the disaster information."
            )

            st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Natural Language Processing–Based Intelligent System "
    "for Disaster-Related Information Extraction and "
    "Automated Situation Summarization from Multisource "
    "Text Data"
)

st.caption(
    "SDG Goal 11 – Sustainable Cities and Communities"
)
