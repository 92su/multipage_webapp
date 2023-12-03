from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie


def app():
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
    #st.set_page_config(page_title="Mandalay City Development Committee", page_icon=":tada:", layout="wide")

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

# use local class
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")

    lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_wkvljkoh.json")
    img_contact_form = Image.open("images/mdy.png")
    img_lottie_animation = Image.open("images/mdy_night.jpeg")
# -----Header Section -----
    with st.container():

        st.subheader("Mandalay Smart City :wave:")
        st.title("An Engineer from Myanmar")
        st.write("I am passionate about coding")
        st.write("[Learn More>](https://python.com)")

        with st.container():
            st.write("---")
            left_column,right_column=st.columns(2)
            with left_column:
                st.header("မန္တလေးမြို့")
                st.write('##')
                st.write(
                """
                မန္တလေးမြို့သည် မြန်မာနိုင်ငံ၏ ဒုတိယအကြီးဆုံးမြို့ဖြစ်ပြီး မန္တလေးတိုင်းဒေသကြီး၏မြို့တော်ဖြစ်သည်။
                ၂၀၁၄ ခုနှစ် စာရင်းအရ လူဦးရေ ၁ ၂၂၅ ၅၅၃ ယောက် ရှိသည်။
                စီးပွားရေးမြို့တော် ရန်ကုန်မြို့ မှ ၃၈၅မိုင် ကွာဝေး၍ ဧရာဝတီမြစ်၏ အရှေ့ဘက်တွင် တည်ရှိသည်။
                ကုန်းဘောင်မင်းဆက် မြန်မာနိုင်ငံ၏ နောက်ဆုံးမင်းနေပြည်တော် ဖြစ်ခဲ့သည်။"""
                )
                st.write("[YouTube Channel>](https://www.youtube.com/watch?v=EViqgpvbrKQ)")
                with right_column:
                    st_lottie(lottie_coding, height=300,key="coding")

# ---- projects ----
    with st.container():
        st.write("____")
        st.header("Our Mandalay")
        st.write("##")
        image_column, text_column = st.columns((1,2))
        with image_column:
            st.image(img_lottie_animation)
        # insert image_column
        with text_column:
            st.subheader("Visit Mandalay")
            st.write(
            """
            You can learn more about Mandalay City
            """
            )
            st.markdown("Watch Video...](https://www.youtube.com/watch?v=gW_tkS45M1I)")


        with st.container():
            image_column, text_column = st.columns((1,2))
            with image_column:
                    st.image(img_contact_form)
            with text_column:
                        st.subheader("Welcome to Mandalay")
                        st.write(
                        """
                        You can learn more about Mandalay City
                        """
                        )
                        st.markdown("Watch Video...](https://www.youtube.com/watch?v=gW_tkS45M1I)")

        with st.container():
                            st.write("---")
                            st.header("Get In Touch with Me!")
                            st.write("##")

    # Documentation: https:formsubmit.co/ !!! change email address

                            contact_form = """
                            <form action = "https://formsubmit.co/smasma1992@gmail.com" method = "POST">
                                <input type="hidden" name="_captcha" value="false">
                                <input type = "text" name="name" placeholder = "Your name" required>
                                <input type="email" name="email" placeholder ="Your email" required>
                                <textarea name="message" placeholder="Your message here" required></textarea>
                                <button type="submit">Send</button>
                                </form>
                                """
                            left_column, right_column = st.columns(2)
                            with left_column:
                                st.markdown(contact_form, unsafe_allow_html=True)
                            with right_column:
                                st.empty()
