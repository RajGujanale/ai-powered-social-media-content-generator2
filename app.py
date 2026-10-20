import streamlit as st
import re

st.set_page_config(
    page_title="AI College Event Promoter",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI-Based Social Media Content Creation System")
st.write(
    "Create social media captions, hashtags, calls to action, "
    "and a poster concept for college events."
)

# ---------------------------
# Event details input
# ---------------------------

st.header("1. Enter Event Details")

with st.form("event_form"):
    event_name = st.text_input(
        "Event Name",
        placeholder="e.g. AI and Robotics Workshop"
    )

    purpose = st.text_area(
        "Event Purpose",
        placeholder="Explain what participants will learn or experience."
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="e.g. Engineering students and beginners"
    )

    event_date = st.text_input(
        "Event Date",
        placeholder="e.g. 15 November 2026"
    )

    venue = st.text_input(
        "Venue",
        placeholder="e.g. College Auditorium"
    )

    important_details = st.text_area(
        "Important Details",
        placeholder=(
            "Enter timings, registration link, speaker names, "
            "organizer, fees, contact details, etc."
        )
    )

    submitted = st.form_submit_button(
        "Generate Promotional Content",
        type="primary"
    )

# ---------------------------
# Content generation
# ---------------------------

def make_hashtag(text):
    words = re.findall(r"[A-Za-z0-9]+", text)
    return "".join(word.capitalize() for word in words)


def build_captions(name, purpose, audience, date, venue, details):
    formal = (
        f"📢 {name}\n\n"
        f"You are invited to participate in {name}. "
        f"{purpose}\n\n"
        f"Designed for: {audience}\n"
        f"📅 Date: {date}\n"
        f"📍 Venue: {venue}\n\n"
        f"{details}\n\n"
        "We look forward to your participation."
    )

    creative = (
        f"🚀 Ideas. Innovation. Inspiration!\n\n"
        f"Get ready for {name}!\n"
        f"{purpose}\n\n"
        f"Bring your curiosity and discover new possibilities.\n"
        f"📅 {date} | 📍 {venue}\n"
        f"👥 For: {audience}\n\n"
        f"{details}"
    )

    student = (
        f"Hey students! 👋🔥\n\n"
        f"Who's ready for {name}?\n\n"
        f"{purpose}\n\n"
        f"📅 When: {date}\n"
        f"📍 Where: {venue}\n"
        f"🎯 Perfect for: {audience}\n\n"
        f"{details}\n\n"
        "Tag your friends and spread the word! 🙌"
    )

    return formal, creative, student


def verify_content(captions, supplied_values):
    """
    Check that required event facts are represented in the
    captions. This is a basic consistency check, not an AI
    fact-checking system.
    """
    combined = "\n".join(captions).lower()
    results = []

    for label, value in supplied_values.items():
        if value.strip():
            present = value.strip().lower() in combined
            results.append({
                "Detail": label,
                "Supplied Value": value,
                "Check": "Present" if present else "Review needed"
            })

    return results


if submitted:
    required = {
        "Event Name": event_name,
        "Purpose": purpose,
        "Target Audience": audience,
        "Event Date": event_date,
        "Venue": venue
    }

    missing = [
        key for key, value in required.items()
        if not value.strip()
    ]

    if missing:
        st.error(
            "Please fill in these required fields: "
            + ", ".join(missing)
        )
    else:
        formal, creative, student = build_captions(
            event_name,
            purpose,
            audience,
            event_date,
            venue,
            important_details
        )

        captions = [formal, creative, student]

        st.session_state["captions"] = captions
        st.session_state["event"] = {
            "name": event_name,
            "purpose": purpose,
            "audience": audience,
            "date": event_date,
            "venue": venue,
            "details": important_details
        }

# ---------------------------
# Display captions
# ---------------------------

if "captions" in st.session_state:
    event = st.session_state["event"]
    captions = st.session_state["captions"]

    st.header("2. Generated Social Media Captions")

    tabs = st.tabs([
        "Formal Tone",
        "Creative Tone",
        "Student-Friendly Tone"
    ])

    labels = [
        "Formal",
        "Creative",
        "Student-Friendly"
    ]

    for tab, caption, label in zip(tabs, captions, labels):
        with tab:
            st.text_area(
                f"{label} Caption",
                value=caption,
                height=260,
                key=f"caption_{label}"
            )

            st.download_button(
                f"Download {label} Caption",
                data=caption,
                file_name=f"{label.lower()}_caption.txt",
                mime="text/plain",
                key=f"download_{label}"
            )

    # ---------------------------
    # Hashtags and CTA
    # ---------------------------

    st.header("3. Hashtags and Call to Action")

    event_tag = make_hashtag(event["name"])
    audience_tag = make_hashtag(event["audience"])

    hashtags = [
        "#" + event_tag,
        "#" + audience_tag,
        "#CollegeEvents",
        "#CampusLife",
        "#StudentCommunity",
        "#LearnAndGrow",
        "#Innovation"
    ]

    hashtag_text = " ".join(dict.fromkeys(hashtags))

    st.text_area(
        "Suggested Hashtags",
        value=hashtag_text,
        height=90
    )

    cta = (
        f"Be part of {event['name']} on {event['date']} "
        f"at {event['venue']}! "
        "Register now using the official registration link "
        "or contact the event organizers for details."
    )

    st.text_area("Call to Action", value=cta, height=100)

    # ---------------------------
    # Fact consistency check
    # ---------------------------

    st.header("4. Event Detail Verification")

    supplied = {
        "Event Name": event["name"],
        "Purpose": event["purpose"],
        "Target Audience": event["audience"],
        "Event Date": event["date"],
        "Venue": event["venue"]
    }

    checks = verify_content(captions, supplied)

    st.dataframe(
        checks,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Verification checks whether supplied details appear in the "
        "captions. Human review is still required to confirm correctness."
    )

    # ---------------------------
    # Poster concept
    # ---------------------------

    st.header("5. Promotional Poster Concept")

    st.write("Use this concept as the event's poster layout.")

    st.markdown(
        f"""
        # 🎓 {event['name']}

        **{event['purpose']}**

        📅 **Date:** {event['date']}

        📍 **Venue:** {event['venue']}

        👥 **Target Audience:** {event['audience']}

        {event['details']}

        ---

        **JOIN US — LEARN, CONNECT, INNOVATE!**
        """
    )

    st.info(
        "Poster concept only: this section generates a text layout, "
        "not an AI-generated image file."
    )

    # ---------------------------
    # Complete content package
    # ---------------------------

    st.header("6. Download Promotional Content Package")

    report = f"""
COLLEGE EVENT PROMOTIONAL CONTENT PACKAGE

EVENT DETAILS
Event Name: {event['name']}
Purpose: {event['purpose']}
Target Audience: {event['audience']}
Date: {event['date']}
Venue: {event['venue']}
Important Details: {event['details']}

FORMAL CAPTION
{captions[0]}

CREATIVE CAPTION
{captions[1]}

STUDENT-FRIENDLY CAPTION
{captions[2]}

HASHTAGS
{hashtag_text}

CALL TO ACTION
{cta}

POSTER CONCEPT
{event['name']}
{event['purpose']}
Date: {event['date']}
Venue: {event['venue']}
Audience: {event['audience']}

VERIFICATION
""" + "\n".join(
        f"{row['Detail']}: {row['Check']}"
        for row in checks
    )

    st.download_button(
        "Download Complete Content Package",
        data=report,
        file_name="college_event_promotion.txt",
        mime="text/plain"
    )

st.divider()
st.caption(
    "College project prototype | Rule-based content generation | "
    "Basic consistency verification"
)