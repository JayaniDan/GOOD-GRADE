import streamlit as st

from utils.calculations import (
    calculate_current_grade,
    calculate_evaluated_percentage,
    calculate_remaining_percentage,
    calculate_needed_grade,
    calculate_best_possible_grade,
    is_target_possible,
)


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Good Grade",
    page_icon="🎓",
    layout="wide",
)


# -------------------------
# SESSION STATE
# -------------------------

if "subjects" not in st.session_state:
    st.session_state.subjects = []


# -------------------------
# HEADER
# -------------------------

st.title("GOOD GRADE")

st.caption("Your grades. Your goals. Under control.")

st.divider()


# -------------------------
# SEMESTER GOAL
# -------------------------

st.subheader("Your semester")

target_average = st.number_input(
    "What average do you want to maintain?",
    min_value=0.0,
    max_value=10.0,
    value=8.5,
    step=0.1,
)


# -------------------------
# ADD SUBJECT
# -------------------------

st.subheader("Add a subject")

subject_name = st.text_input(
    "Subject name",
    placeholder="Example: Financial Engineering",
)

if st.button("Add subject"):

    if subject_name.strip():

        new_subject = {
            "name": subject_name.strip(),
            "evaluations": [],
        }

        st.session_state.subjects.append(new_subject)

        st.success(
            f"{subject_name} was added successfully."
        )

        st.rerun()

    else:

        st.warning("Please enter a subject name.")


st.divider()


# -------------------------
# SUBJECTS
# -------------------------

st.subheader("My subjects")

if len(st.session_state.subjects) == 0:

    st.info(
        "You haven't added any subjects yet."
    )

else:

    for index, subject in enumerate(
        st.session_state.subjects
    ):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(
                    f"### {subject['name']}"
                )

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{index}",
                ):

                    st.session_state.subjects.pop(
                        index
                    )

                    st.rerun()

            evaluations = subject[
                "evaluations"
            ]

            if evaluations:

                current_grade = (
                    calculate_current_grade(
                        evaluations
                    )
                )

                evaluated = (
                    calculate_evaluated_percentage(
                        evaluations
                    )
                )

                remaining = (
                    calculate_remaining_percentage(
                        evaluations
                    )
                )

                needed = (
                    calculate_needed_grade(
                        target_average,
                        evaluations,
                    )
                )

                best_possible = (
                    calculate_best_possible_grade(
                        evaluations
                    )
                )

                possible = (
                    is_target_possible(
                        target_average,
                        evaluations,
                    )
                )

                col_a, col_b, col_c = (
                    st.columns(3)
                )

                col_a.metric(
                    "Current grade",
                    f"{current_grade:.2f}",
                )

                col_b.metric(
                    "Evaluated",
                    f"{evaluated:.0f}%",
                )

                col_c.metric(
                    "Remaining",
                    f"{remaining:.0f}%",
                )

                st.write(
                    f"Best possible grade: "
                    f"**{best_possible:.2f}**"
                )

                if needed is not None:

                    if possible:

                        st.success(
                            f"You need an average of "
                            f"{max(needed, 0):.2f} "
                            f"in the remaining evaluations "
                            f"to finish with "
                            f"{target_average:.1f}."
                        )

                    else:

                        st.error(
                            f"Reaching "
                            f"{target_average:.1f} "
                            f"is no longer mathematically "
                            f"possible."
                        )

            else:

                st.caption(
                    "No evaluations added yet."
                )
