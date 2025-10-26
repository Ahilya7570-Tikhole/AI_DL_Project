import streamlit as st
import base64
import io

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Real Adapt: Dynamic Ad Generation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PLACEHOLDER URLS ---
PLACEHOLDER_MP4_URL = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4" 
LOGO_URL = "https://img.icons8.com/plasticine/100/adapt.png" 

# --- ICONS & COLOR VARIABLES (MISSING VARIABLES ADDED HERE) ---
ACCENT_COLOR = "#CD7F32" # Richer Bronze/Sienna
ICON_FORM = f"https://img.icons8.com/ios-filled/50/{ACCENT_COLOR[1:]}/document.png"      # User Input
ICON_PREVIEW = f"https://img.icons8.com/ios-filled/50/{ACCENT_COLOR[1:]}/eye.png"        # Preview Mode
ICON_LANGUAGE = f"https://img.icons8.com/ios-filled/50/{ACCENT_COLOR[1:]}/globe--v1.png" # Multi-Language
ICON_DOWNLOAD = f"https://img.icons8.com/ios-filled/50/{ACCENT_COLOR[1:]}/download.png"  # Download & Share

# --- New Color Palette Variables (For Primary Buttons and Inputs) ---
COLOR_PRIMARY_BUTTON_BG = "#4CAF50"      # Vibrant Green for buttons (like your image)
COLOR_PRIMARY_BUTTON_SHADOW = "#388E3C"  # Darker Green for button shadow
COLOR_PRIMARY_TEXT_COLOR = "white"       # White text for the buttons
COLOR_PRIMARY_ACCENT = "#FFEA00"         # Gold/Amber for headings/accents
COLOR_SECONDARY_ACCENT = "#00FFFF"       # Cyan for input labels


# --- 2. CUSTOM CSS FOR AESTHETICS (ENHANCED) ---
st.markdown(f"""
<style>
    /* General App Background */
    .stApp {{
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #E0E0FF;
        font-family: 'Inter', sans-serif;
    }}

    /* Global Headings */
    h1, h2, h3, h4, .st-emotion-cache-10trblm {{
        color: {COLOR_PRIMARY_ACCENT} !important; 
    }}

    /* Title Styling */
    .centered-title {{
        text-align: center;
        font-size: 3.5em; 
        font-weight: 900;
        color: {COLOR_PRIMARY_ACCENT} !important; 
        text-shadow: 0 0 5px rgba(255, 215, 0, 0.7), 0 0 10px rgba(255, 215, 0, 0.4);
        padding-top: 50px;
        margin-bottom: 20px;
    }}

    /* Header styling */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        margin-bottom: 30px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .logo {{
        font-size: 2.5em; 
        font-weight: 900; 
        color: {COLOR_PRIMARY_ACCENT}; 
        display: flex;
        align-items: center;
        text-shadow: 2px 2px 5px rgba(255, 234, 0, 0.4); 
    }}
    .logo img {{
        margin-right: 10px;
        border-radius: 50%;
        filter: drop-shadow(0 0 8px rgba(255,234,0,0.8)); 
    }}

    /* Default Nav Button Style (Home/Features) */
    div[data-testid="column"] button {{ 
        background-color: transparent !important;
        color: #C0C0D8 !important;
        border: none !important;
        font-weight: bold;
        font-size: 1.1em;
        padding: 0.8em 0.5em !important;
        margin: 0;
        transition: color 0.3s, background-color 0.3s;
    }}
    div[data-testid="column"] button:hover {{
        color: {COLOR_PRIMARY_ACCENT} !important;
        background-color: rgba(255, 234, 0, 0.1) !important;
    }}
    
    /* --- PRIMARY ACTION BUTTON STYLING (Login/Sign Up, Create Ad, Generate Another Ad) --- */
    /* Target buttons with specific keys or within the action-button-container */
    div[data-testid="stVerticalBlock"] .stButton > button:has(div[data-testid="baseButton-nav_login"]),
    .action-button-container .stButton > button,
    button[data-testid="baseButton-nav_login"],
    button[data-testid="baseButton-generate_button"],
    button[data-testid="baseButton-generate_another"]
    {{
        /* Use !important liberally for Streamlit overrides */
        background-color: {COLOR_PRIMARY_BUTTON_BG} !important; 
        color: {COLOR_PRIMARY_TEXT_COLOR} !important; 
        border: none !important; 
        border-radius: 12px !important; /* Highly rounded corners for exact match */
        font-weight: 700 !important;
        text-transform: uppercase !important; 
        padding: 10px 20px !important; 
        height: 50px !important; 
        
        /* 3D Box shadow to match the image */
        box-shadow: 0 8px 0 0 {COLOR_PRIMARY_BUTTON_SHADOW}, /* Darker green shadow beneath */
                    0 4px 10px rgba(0, 0, 0, 0.3); /* General softer shadow */
        transition: all 0.15s ease-out; /* Smooth transition */
        display: flex;
        justify-content: center;
        align-items: center;
        line-height: 1; /* Fix vertical centering */
    }}
    
    /* Hover state for action buttons (Button presses down slightly) */
    div[data-testid="stVerticalBlock"] .stButton > button:hover,
    .action-button-container .stButton > button:hover
    {{
        background-color: {COLOR_PRIMARY_BUTTON_SHADOW} !important;
        box-shadow: 0 4px 0 0 #2e7d32, /* Smaller shadow on hover */
                    0 2px 5px rgba(0, 0, 0, 0.3);
        transform: translateY(4px); /* Move button down slightly */
    }}

    /* Active (clicked) state for action buttons (Button is fully pressed) */
    div[data-testid="stVerticalBlock"] .stButton > button:active,
    .action-button-container .stButton > button:active
    {{
        background-color: #2e7d32 !important; 
        box-shadow: none; /* No shadow when pressed */
        transform: translateY(8px); /* Fully pressed state */
    }}
    
    .action-button-container {{
        display: flex;
        align-items: flex-end; 
        padding-top: 10px; 
        height: 100%;
        width: 100%; 
        margin: 0 !important;
    }}
    
    /* Card Containers - Glassmorphism Effect for Input Area */
    /* Target the container wrapping the input widgets in col1 */
    [data-testid="stVerticalBlock"] > div:has([data-testid="stTextInput"], [data-testid="stRadio"], [data-testid="stSelectbox"], [data-testid="stFileUploader"]) {{
        background: rgba(45, 45, 80, 0.4); 
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px); 
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.4); /* Cyan Border */
        margin-bottom: 20px;
    }}

    /* Input Labels Style (Product Name, Target Audience, etc.) */
    div[data-testid^="stWidgetLabel"] > label {{
        font-size: 1.15em; 
        font-weight: 700; 
        color: {COLOR_SECONDARY_ACCENT} !important; /* Cyan color */
        margin-bottom: 5px; 
        padding-top: 10px; 
    }}
    
    /* Text Input, Text Area, Selectbox Containers (The input box itself) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    div[data-testid="stSelectbox"] div[role="combobox"]
    {{
        background-color: rgba(48, 43, 99, 0.6); /* Darker purple transparent background */
        color: white !important; 
        border: 2px solid {COLOR_SECONDARY_ACCENT}; /* Cyan border */
        border-radius: 8px;
        padding: 10px;
        transition: border-color 0.3s, box-shadow 0.3s;
    }}

    /* Focus state for inputs */
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus
    {{
        border-color: {COLOR_PRIMARY_ACCENT}; 
        box-shadow: 0 0 10px {COLOR_PRIMARY_ACCENT};
        outline: none;
    }}

    /* Placeholder text color */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder
    {{
        color: #A0A0FF; 
        opacity: 0.7;
    }}

    /* Radio Button Styling (for Tone/Emotion) */
    div[data-testid="stRadio"] label {{
        background-color: rgba(48, 43, 99, 0.4);
        border: 1px solid #444;
        border-radius: 6px;
        padding: 5px 10px;
        margin: 0 5px 5px 0;
        cursor: pointer;
        transition: background-color 0.2s;
    }}
    
     /*Selected Radio Button ring */
    div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child {{
        border: 2px solid {COLOR_PRIMARY_ACCENT} !important; 
    }}
    
    /* File Uploader styling */
    div[data-testid="stFileUploader"] {{
        border: 2px dashed rgba(0, 255, 255, 0.5); 
        border-radius: 8px;
        padding: 15px;
        background-color: rgba(48, 43, 99, 0.3);
    }}
    
    /* === FEATURE CARD STYLES (Retained for completeness) === */
    .features-section-container {{
        padding: 60px 0; 
        background-color: #E6F3F7; 
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
    }}
    
    .feature-card {{
        background-color: #F8F8F8;
        border-radius: 15px; 
        padding: 30px; 
        text-align: center;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        color: #333333; 
        min-height: 480px; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start; 
        border: 1px solid rgba(205, 127, 50, 0.2);
    }}
    .feature-card:hover {{
        transform: translateY(-8px); 
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
    }}
    .feature-card .icon-circle {{
        background-color: {ACCENT_COLOR}; 
        border-radius: 15px; 
        width: 80px;
        height: 80px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 25px auto;
    }}
    .feature-card .icon-circle img {{
        width: 50px; 
        height: 50px;
        filter: brightness(0) invert(1);
    }}
    .feature-card h3 {{
        color: #1A1A2E !important; 
        font-size: 1.4em;
        margin-bottom: 20px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .feature-card p {{
        font-size: 0.9em; 
        line-height: 1.7;
        color: #555555;
        margin-bottom: 10px;
        text-align: center;
        flex-grow: 1; 
    }}
    .feature-card .more-btn {{
        margin-top: auto; 
        display: block; 
        text-align: center;
        text-decoration: none;
        color: {ACCENT_COLOR};
        font-weight: bold;
        padding: 10px 15px;
        border: none; 
        border-bottom: 2px solid {ACCENT_COLOR}; 
        border-radius: 0;
        transition: color 0.3s;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }}
    .feature-card .more-btn:hover {{
        color: #9f6327;
    }}
    
</style>
""", unsafe_allow_html=True)

# --- 3. DOWNLOAD HELPERS ---
def get_text_download_link(content, filename, text):
    """Generates a styled text file download link."""
    b64 = base64.b64encode(content.encode()).decode()
    # Apply primary button style to download links as well
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="stDownloadButton"><button style="background-color: {COLOR_PRIMARY_BUTTON_BG}; color: {COLOR_PRIMARY_TEXT_COLOR}; border-radius: 12px; font-weight: 700; text-transform: uppercase; padding: 10px 20px; box-shadow: 0 4px 0 0 #2e7d32;">{text}</button></a>'
    return href

def get_mp4_download_link(mp4_url, filename, text):
    """Generates a styled MP4 download link (for pre-existing MP4s)."""
    # Apply primary button style to download links as well
    return f'<a href="{mp4_url}" download="{filename}" class="stDownloadButton"><button style="background-color: {COLOR_PRIMARY_BUTTON_BG}; color: {COLOR_PRIMARY_TEXT_COLOR}; border-radius: 12px; font-weight: 700; text-transform: uppercase; padding: 10px 20px; box-shadow: 0 4px 0 0 #2e7d32;">{text}</button></a>'


# --- 4. PREVIEW GENERATOR FUNCTION ---
def generate_preview(ad_type, ad_data):
    headline = ad_data.get('headline', 'Generated Ad Headline')
    body = ad_data.get('body', 'Generated body text...')
    cta = ad_data.get('cta', 'Learn More')
    
    if ad_type == "Social Media Post":
        html = f"""
        <div class="social-post-preview" style="background-color: #1A1A2E; padding: 20px; border-radius: 10px; border: 1px solid rgba(255,215,0,0.3);">
            <p style="color:#FFF; font-weight:bold; margin-bottom: 5px;">Real Adapt Ads</p>
            <p style="font-size:0.8em; color:#AAA;">Sponsored</p>
            <hr style="border-top: 1px solid #333;">
            <p style="margin-top: 10px;">{body}</p>
            <img src="{st.session_state.get('image_url', 'https://picsum.photos/400/250?random=3')}" style="width:100%; height:auto; margin-top:10px; border-radius:4px;">
            <p style="text-align:right; margin-top:10px;">
                <button style="background-color:{COLOR_PRIMARY_BUTTON_BG}; color:{COLOR_PRIMARY_TEXT_COLOR}; padding: 5px 15px; border: none; border-radius: 4px; cursor:pointer;">{cta}</button>
            </p>
        </div>
        """
    elif ad_type == "Google Search Ad":
        html = f"""
        <div class="search-ad-preview" style="background-color: #1A1A2E; padding: 15px; border-radius: 10px; border: 1px solid rgba(255,215,0,0.3);">
            <span style="background-color:{COLOR_PRIMARY_BUTTON_BG}; color:{COLOR_PRIMARY_TEXT_COLOR}; padding: 2px 5px; border-radius: 3px; font-size: 0.8em; margin-right: 5px;">Ad</span>
            <span style="color: #6a6a6a; font-size: 0.9em;">www.realadapt.com</span>
            <div style="font-size: 1.1em; color: {COLOR_SECONDARY_ACCENT}; margin-top: 5px; font-weight: bold;">{headline}</div>
            <div style="font-size: 0.9em; color: #C0C0D8; margin-top: 5px;">{body.split('.')[0]}. {cta}</div>
        </div>
        """
    elif ad_type == "Video Ad":
        return None 
    else:
        html = f'<div class="output-box" style="padding: 15px; border: 1px dashed {COLOR_PRIMARY_ACCENT}; border-radius: 10px;"><h3>{headline}</h3><p>{body}</p><strong>CTA:</strong> {cta}</div>'
        
    return html

# --- 5. SESSION STATE NAVIGATION SETUP ---

# 1. Initialize the page state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# 2. Function to switch the page state
def navigate_to(page_name):
    st.session_state['current_page'] = page_name

# 3. Read the current page from the state
current_page = st.session_state['current_page']

# Custom Header 
col_logo, col_nav, col_login = st.columns([1, 1, 0.5], gap="medium")

with col_logo:
    st.markdown(f"""
    <div class="logo">
        <img src="{LOGO_URL}" width="45" height="45">
        Real Adapt
    </div>
    """, unsafe_allow_html=True)

with col_nav:
    # Use native Streamlit buttons with callbacks for reliable navigation
    nav_col1, nav_col2 = st.columns([0.2, 0.8])
    with nav_col1:
        st.button("Home", key="nav_home", on_click=navigate_to, args=('home',), use_container_width=True)
    with nav_col2:
        st.button("Features", key="nav_features", on_click=navigate_to, args=('features',), use_container_width=False)


with col_login:
    # This button uses the new green styling
    if st.button("LOGIN / SIGN UP", key="nav_login", help="Click to Login or Create an Account"):
        navigate_to('login_signup')

st.markdown('<div class="header-container" style="border-top: none; padding-top: 0; margin-top: 0;"></div>', unsafe_allow_html=True) # Separator


# --- PAGE CONTENT RENDERING ---

if current_page == "home":
    
    st.markdown('<div class="centered-title">Dynamic Ad Creation ⚡</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: center; color: #C0C0D8; margin-bottom: 40px;">Enter your product details to receive instant, platform-optimized ad copy.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<h3>Ad Input Parameters</h3>", unsafe_allow_html=True)

        # Inputs now benefit from the CSS styling defined above
        product_name = st.text_input("Product Name:", placeholder="e.g., Ultra-Fast NVMe SSD", key='product_name')
        target_audience = st.text_input("Target Audience:", placeholder="e.g., PC Gamers, Video Editors", key='target_audience')

        st.markdown("<h4>Tone/Emotion:</h4>", unsafe_allow_html=True)
        emotion_tone = st.radio(
            "",
            ('Funny', 'Urgent', 'Inspiring', 'Luxury', 'Excitement', 'Trust'),
            horizontal=True,
            key='tone_radio'
        )

        ad_type = st.selectbox("Output Format/Platform (Ad Type):", 
            ('Social Media Post', 'Google Search Ad', 'Email Ad', 'Banner Ad', 'Video Ad', 'Tagline Only'), 
            key='ad_type')
            
        tagline = st.text_input("Key Benefit/Tagline Idea (Optional):", placeholder="e.g., Load games 5x faster", key='tagline')
        
        language = st.selectbox("Language:", ('English', 'Spanish', 'French', 'Hindi'), key='language')
        
        call_to_action = st.text_input("Call to Action (e.g., SHOP NOW):", placeholder="e.g., GET YOURS TODAY", key='cta_hint')
        
        uploaded_file = st.file_uploader("Upload Ad Image (Optional, for Visual Context):", type=['png', 'jpg', 'jpeg'], key='image_upload')
        if uploaded_file is not None:
              st.session_state['uploaded_image'] = uploaded_file
              st.session_state['image_url'] = f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}"
        else:
            if 'image_url' in st.session_state:
                del st.session_state['image_url']


        # Action Buttons
        col_btn1, col_btn2, _ = st.columns([0.4, 0.4, 1.2]) 
        
        with col_btn1:
            st.markdown('<div class="action-button-container">', unsafe_allow_html=True)
            if st.button("CREATE AD", key='generate_button', use_container_width=True):
                if product_name and target_audience:
                    generated_ad_data = {
                        'headline': f"🚀 {product_name}: The {emotion_tone} Speed You Need!",
                        'body': f"Stop waiting and start working! Our {product_name} delivers blazing-fast performance for {target_audience}. {tagline if tagline else 'Upgrade your system now and feel the difference.'}",
                        'cta': call_to_action if call_to_action else 'Click Here',
                        'raw_copy': (
                            f"Headline: 🚀 {product_name}: The {emotion_tone} Speed You Need!\n"
                            f"Body: Stop waiting and start working! Our {product_name} delivers blazing-fast performance for {target_audience}. "
                            f"{tagline if tagline else 'Upgrade your system now and feel the difference.'}\n"
                            f"Call to Action: {call_to_action if call_to_action else 'Click Here'}\n"
                            f"Tone: {emotion_tone}, Language: {language}"
                        )
                    }
                    st.session_state['generated_ad_data'] = generated_ad_data
                else:
                    st.error("Please enter a **Product Name** and **Target Audience** to generate an ad.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_btn2:
            st.markdown('<div class="action-button-container">', unsafe_allow_html=True)
            if st.button("GENERATE NEW AD", key='generate_another', use_container_width=True):
                st.session_state.pop('generated_ad_data', None)
                st.session_state.pop('uploaded_image', None)
                st.session_state.pop('image_url', None)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("<h3>Live Ad Preview:</h3>", unsafe_allow_html=True) 
        
        ad_data = st.session_state.get('generated_ad_data', None)

        if ad_data:
            if ad_type == "Video Ad":
                st.info("Video generation simulated. In a real app, the server would render the MP4 here.")
                st.markdown('<div class="stVideo">', unsafe_allow_html=True)
                st.video(PLACEHOLDER_MP4_URL) 
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<h4>Video Script/Copy:</h4>", unsafe_allow_html=True)
                st.code(ad_data['raw_copy'], language='text')
                
                # Download and Share buttons for Video Ad
                st.markdown("<br>", unsafe_allow_html=True)
                col_dl_vid, col_share_vid, _ = st.columns([0.4, 0.4, 1.2])
                with col_dl_vid:
                    # Using get_mp4_download_link which has inline button styling now
                    st.markdown(
                        get_mp4_download_link(PLACEHOLDER_MP4_URL, "real_adapt_ad.mp4", "⬇️ DOWNLOAD AD (.MP4)"), 
                        unsafe_allow_html=True
                    )
                with col_share_vid:
                    # Share button uses the primary button style
                    if st.button("🔗 SHARE AD", key='share_ad_vid', use_container_width=True): 
                         st.success("Ad link copied to clipboard! (Simulated)")
                
            else:
                st.markdown(
                    generate_preview(ad_type, ad_data),
                    unsafe_allow_html=True
                )
                st.markdown("<h4>Raw Copy:</h4>", unsafe_allow_html=True)
                st.code(ad_data['raw_copy'], language='text')

                # Download and Share buttons for Text/Image Ad
                st.markdown("<br>", unsafe_allow_html=True)
                col_dl_txt, col_share_txt, _ = st.columns([0.4, 0.4, 1.2])
                download_text = ad_data['raw_copy'].replace('**', '').replace('\n\n', '\n').replace('\n', '\r\n')
                with col_dl_txt:
                    # Using get_text_download_link which has inline button styling now
                    st.markdown(
                        get_text_download_link(download_text, "real_adapt_ad_copy.txt", "⬇️ DOWNLOAD COPY (.TXT)"), 
                        unsafe_allow_html=True
                    )
                with col_share_txt:
                    # Share button uses the primary button style
                    if st.button("🔗 SHARE AD", key='share_ad_txt', use_container_width=True): 
                         st.success("Ad copy link copied to clipboard! (Simulated)")

        else:
            st.markdown('<div class="output-box" style="padding: 50px; text-align: center; border: 2px dashed #302b63; border-radius: 10px;">Click **CREATE AD** to see your platform preview here!</div>', unsafe_allow_html=True)


# --- Features Page Content ---
elif current_page == "features":
    
    st.markdown("""
        <div style="text-align: center; color: #FFD700; padding-top: 50px;">
            <h2>KEY FEATURES</h2>
            <p style="color: #C0C0D8; font-size: 1.1em; margin-bottom: 50px;">"Transforming Ideas into Impactful Ads, Instantly."</p>
        </div>
    """, unsafe_allow_html=True)

    
    # 2. Use Streamlit's native column layout for guaranteed side-by-side rendering
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    # --- CARD 1: USER INPUT ---
    with col1:
        # ICON_FORM is now defined at the top, resolving the NameError
        card_1_html = f"""
        <div class="feature-card">
            <div class="icon-circle"><img src="{ICON_FORM}" alt="Input Form"></div>
            <h3>USER INPUT</h3>
            <p>Allows users to enter product name, brand description, and define a clear target audience such as students or professionals.</p>
            <p>Provides options to choose a tone or emotion like funny, urgent, or luxury, and enables selection of ad type.</p>
            <a href="#" class="more-btn">LEARN MORE</a>
        </div>
        """
        st.markdown(card_1_html, unsafe_allow_html=True)
        
    # --- CARD 2: PREVIEW MODE ---
    with col2:
        card_2_html = f"""
        <div class="feature-card">
            <div class="icon-circle"><img src="{ICON_PREVIEW}" alt="Preview Mode"></div>
            <h3>PREVIEW MODE</h3>
            <p>Shows the generated ads in realistic social media mockups instantly, offering platform-specific previews (Instagram, Facebook).</p>
            <p>The formatting adapts to match banner, post, or search advertisement layouts, helping users visualize the campaign.</p>
            <a href="#" class="more-btn">LEARN MORE</a>
        </div>
        """
        st.markdown(card_2_html, unsafe_allow_html=True)

    # --- CARD 3: MULTI-LANGUAGE ---
    with col3:
        card_3_html = f"""
        <div class="feature-card">
            <div class="icon-circle"><img src="{ICON_LANGUAGE}" alt="Multi-Language Support"></div>
            <h3>MULTI-LANGUAGE</h3>
            <p>Creates ad content in English as well as popular regional languages, helping brands connect with audiences beyond English-speaking groups.</p>
            <p>Allows ads to be customized for local markets, expanding the campaign reach with multilingual advertising features.</p>
            <a href="#" class="more-btn">LEARN MORE</a>
        </div>
        """
        st.markdown(card_3_html, unsafe_allow_html=True)
        
    # --- CARD 4: DOWNLOAD & SHARE ---
    with col4:
        card_4_html = f"""
        <div class="feature-card">
            <div class="icon-circle"><img src="{ICON_DOWNLOAD}" alt="Download & Share"></div>
            <h3>DOWNLOAD & SHARE</h3>
            <p>Lets users download generated video ads directly in .mp4 format or save raw ad copy (.txt).</p>
            <p>Includes quick-share buttons to copy links or send ads across platforms, ensuring campaigns can be exported and reused.</p>
            <a href="#" class="more-btn">LEARN MORE</a>
        </div>
        """
        st.markdown(card_4_html, unsafe_allow_html=True)

    # 3. Close the full-width background strip container
    st.markdown('</div>', unsafe_allow_html=True)


# --- Login/Sign Up Page Content ---
elif current_page == "login_signup":
    st.markdown("<h1>👋 WELCOME To REAL ADAPT!</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: center;">Securely manage your dynamic ad campaigns.</p>', unsafe_allow_html=True)
    
    login_or_signup = st.radio("Choose an option:", ("LOGIN", "SIGN UP"), horizontal=True, key='login_radio') # All caps
    

    if login_or_signup == "LOGIN":
        st.markdown("<h4 style='color:#00FFFF;'>LOG IN TO YOUR ACCOUNT</h4>", unsafe_allow_html=True)
        email = st.text_input("Email Address:", key="login_email_page")
        password = st.text_input("Password:", type="password", key="login_password_page")
        st.markdown(f'<a href="#" onclick="window.parent.postMessage(\'streamlit:sendMessage\', \'forgot_password\')" style="color:#C0C0D8; font-size: 0.9em;">Forgot Password?</a><br><br>', unsafe_allow_html=True)
        
        # This button also uses the primary green style
        if st.button("LOG IN", key="login_submit_page", use_container_width=True):
            st.success(f"Log In attempt with {email}. (Front-end only)")
            
    else: # Sign Up
        st.markdown("<h4 style='color:#00FFFF;'>CREATE YOUR ACCOUNT</h4>", unsafe_allow_html=True)
        name = st.text_input("Full Name:", key="signup_name_page")
        email = st.text_input("Email Address:", key="signup_email_page")
        password = st.text_input("Create Password:", type="password", key="signup_password_page")
        password_confirm = st.text_input("Confirm Password:", type="password", key="signup_password_confirm_page")
        
        # This button also uses the primary green style
        if st.button("SIGN UP", key="signup_submit_page", use_container_width=True):
            if password and password == password_confirm:
                 st.success(f"Sign Up successful for {name}. Please log in! (Front-end only)")
            elif password:
                st.error("Passwords do not match!")
            else:
                 st.error("Please fill in all fields.")

    st.markdown("</div></div>", unsafe_allow_html=True)

# --- Other Pages Placeholder ---
elif current_page in ["privacy", "terms", "forgot_password"]:
    st.header(f"PAGE: {current_page.replace('_', ' ').upper()}")
    st.markdown("---")
    st.info("This is a placeholder page for the full application structure.")


# --- 6. FOOTER (Always visible) ---
st.markdown("""
<br><br>
<div class="footer" style="text-align: center; padding: 10px; font-size: 0.8em; color: #888;">
    © 2024 Real Adapt. All rights reserved. | 
    <a href="javascript:void(0)" onclick="window.parent.postMessage({target: 'streamlit', data: {type: 'setRoute', url: '/?page=privacy'}}, '*')" style="color:#C0C0D8; text-decoration:none;">Privacy Policy</a> | 
    <a href="javascript:void(0)" onclick="window.parent.postMessage({target: 'streamlit', data: {type: 'setRoute', url: '/?page=terms'}}, '*')" style="color:#C0C0D8; text-decoration:none;">Terms of Service</a>
</div>
""", unsafe_allow_html=True)