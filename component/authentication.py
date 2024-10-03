import os
import yaml
from glob import glob
import streamlit as st
import streamlit_authenticator as stauth


def load_config(credential_path):
    with open(credential_path) as file:
        return yaml.safe_load(file)


def save_config(config, credential_path):
    with open(credential_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)


def get_admin_pages(authenticator, config, credential_path):
    def register_new_user_page():
        try:
            roles = list(config["roles"].keys())
            role_of_registered_user = st.selectbox("Role", roles, index=len(roles) - 1)
            (
                email_of_registered_user,
                username_of_registered_user,
                name_of_registered_user,
            ) = authenticator.register_user(
                pre_authorization=False,
                fields={"Username": "Username (id to login)"},
            )
            if email_of_registered_user:
                config["credentials"]["usernames"][username_of_registered_user][
                    "role"
                ] = role_of_registered_user
                save_config(config, credential_path)
                st.success(
                    f"User {username_of_registered_user} registered successfully"
                )
        except Exception as e:
            st.error(e)

    return [
        st.Page(register_new_user_page, title="Register New User"),
    ]


def get_auth_pages(authenticator, config, credential_path):
    def reset_password_page():
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    save_config(config, credential_path)
                    st.success("Password modified successfully")
            except Exception as e:
                st.error(e)

    def logout_func():
        authenticator.logout(location="unrendered")
        # put single page, having the effect to hide other page on routes
        st.navigation([st.Page("app.py")], position="hidden")

    return [
        st.Page(reset_password_page, title="Reset Password"),
        st.Page(logout_func, title="Logout"),
    ]


def init_authentication(credential_path, subpage_path="my_pages"):
    config = load_config(credential_path)

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )
    authenticator.login()

    # Handle authentication
    status = st.session_state["authentication_status"]
    if status is False:
        st.error("Username/password is incorrect")
        st.stop()
    elif status is None:
        st.warning("Please enter your username and password")
        st.stop()

    username = st.session_state["username"]
    role = config["credentials"]["usernames"][username]["role"]
    st.session_state["role"] = role

    # Initialize navigation
    pages = {subpage_path: []}
    page_paths = glob(f"{subpage_path}/*.py")
    for page_path in page_paths:
        page_title = page_path.split(os.sep)[-1].replace(".py", "")
        if config["roles"][role]["page_restrictions"] is not None:
            if page_title not in config["roles"][role]["page_restrictions"]:
                continue
        pages[subpage_path].append(st.Page(page_path, title=page_title))

    if role == "admin":
        pages["admin"] = get_admin_pages(authenticator, config, credential_path)

    pages["auth"] = get_auth_pages(authenticator, config, credential_path)

    nav = st.navigation(pages)
    nav.run()

    return
