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
# GENERAL SETTINGS
# -------------------------

st.subheader("Semester setup")

col1, col2 = st.columns(2)

with col1:
    grade_scale = st.selectbox(
        "Grade scale",
        options=[10, 100],
        format_func=lambda x: f"0 – {x}",
    )

with col2:
    semester_target = st.number_input(
        "Target semester average",
        min_value=0.0,
        max_value=float(grade_scale),
        value=8.5 if grade_scale == 10 else 85.0,
        step=0.1,
    )

st.caption(
    "This is the average you want to maintain across your semester."
)

st.divider()

# -------------------------
# ADD SUBJECT
# -------------------------

st.subheader("Add a subject")

with st.form("add_subject_form"):

    subject_name = st.text_input(
        "Subject name",
        placeholder="Example: Financial Engineering",
    )

    subject_target = st.number_input(
        "Target grade for this subject",
        min_value=0.0,
        max_value=float(grade_scale),
        value=8.5 if grade_scale == 10 else 85.0,
        step=0.1,
    )

    add_subject = st.form_submit_button(
        "Add subject",
        use_container_width=True,
    )

    if add_subject:

        if subject_name.strip():

            st.session_state.subjects.append(
                {
                    "name": subject_name.strip(),
                    "target": subject_target,
                    "evaluations": [],
                }
            )

            st.rerun()

        else:
            st.warning("Enter a subject name.")

# -------------------------
# SUBJECTS
# -------------------------

st.divider()
st.subheader("My subjects")

if not st.session_state.subjects:

    st.info(
        "Add your first subject to start tracking your semester."
    )

else:

    for subject_index, subject in enumerate(
        st.session_state.subjects
    ):

        with st.expander(
            f"{subject['name']}  ·  Target {subject['target']}",
            expanded=True,
        ):

            # -------------------------
            # SUBJECT HEADER
            # -------------------------

            header1, header2 = st.columns([4, 1])

            with header1:
                st.markdown(
                    f"### {subject['name']}"
                )
                st.caption(
                    f"Target grade: {subject['target']}"
                )

            with header2:

                if st.button(
                    "Delete subject",
                    key=f"delete_subject_{subject_index}",
                    use_container_width=True,
                ):

                    st.session_state.subjects.pop(
                        subject_index
                    )

                    st.rerun()

            evaluations = subject["evaluations"]

            # -------------------------
            # CURRENT RESULTS
            # -------------------------

            if evaluations:

                total_configured = sum(
                    evaluation["weight"]
                    for evaluation in evaluations
                )

                current_grade = calculate_current_grade(
                    evaluations
                )

                evaluated = calculate_evaluated_percentage(
                    evaluations
                )

                remaining = calculate_remaining_percentage(
                    evaluations
                )

                needed = calculate_needed_grade(
                    subject["target"],
                    evaluations,
                )

                best_possible = calculate_best_possible_grade(
                    evaluations,
                    max_grade=grade_scale,
                )

                possible = is_target_possible(
                    subject["target"],
                    evaluations,
                    max_grade=grade_scale,
                )

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric(
                    "Current grade",
                    f"{current_grade:.2f}",
                )

                metric2.metric(
                    "Already evaluated",
                    f"{evaluated:.0f}%",
                )

                metric3.metric(
                    "Still pending",
                    f"{remaining:.0f}%",
                )

                st.progress(
                    min(total_configured / 100, 1.0)
                )

                if total_configured < 100:

                    st.caption(
                        f"{total_configured:.0f}% of the grading "
                        f"scheme has been configured."
                    )

                elif total_configured == 100:

                    st.caption(
                        "Your grading scheme is complete."
                    )

                else:

                    st.error(
                        f"Your evaluation percentages add up to "
                        f"{total_configured:.0f}%. They cannot exceed 100%."
                    )

                st.write(
                    f"**Best possible final grade:** "
                    f"{best_possible:.2f}"
                )

                if total_configured <= 100:

                    if needed is not None:

                        if possible:

                            if needed <= 0:

                                st.success(
                                    "Your target is already secured "
                                    "based on your current results."
                                )

                            else:

                                st.success(
                                    f"You need an average of "
                                    f"**{needed:.2f}** in the remaining "
                                    f"evaluations to finish this subject "
                                    f"with **{subject['target']:.2f}**."
                                )

                        else:

                            st.error(
                                f"Your target of "
                                f"**{subject['target']:.2f}** is no longer "
                                f"mathematically possible. Your best "
                                f"possible result is "
                                f"**{best_possible:.2f}**."
                            )

            else:

                st.info(
                    "No evaluations yet. Add the grading scheme below."
                )

            # -------------------------
            # EVALUATION LIST
            # -------------------------

            if evaluations:

                st.markdown("#### Evaluations")

                for evaluation_index, evaluation in enumerate(
                    evaluations
                ):

                    ev1, ev2, ev3, ev4 = st.columns(
                        [3, 1, 1.5, 1]
                    )

                    with ev1:
                        st.write(
                            f"**{evaluation['name']}**"
                        )

                    with ev2:
                        st.write(
                            f"{evaluation['weight']:.0f}%"
                        )

                    with ev3:

                        if evaluation["grade"] is None:
                            st.write("Pending")
                        else:
                            st.write(
                                f"{evaluation['grade']:.2f}"
                            )

                    with ev4:

                        if st.button(
                            "Remove",
                            key=(
                                f"remove_{subject_index}_"
                                f"{evaluation_index}"
                            ),
                        ):

                            subject["evaluations"].pop(
                                evaluation_index
                            )

                            st.rerun()

            # -------------------------
            # ADD EVALUATION
            # -------------------------

            st.markdown("#### Add evaluation")

            with st.form(
                f"evaluation_form_{subject_index}"
            ):

                evaluation_name = st.text_input(
                    "Evaluation name",
                    placeholder="Example: Midterm 1",
                    key=f"evaluation_name_{subject_index}",
                )

                evaluation_weight = st.number_input(
                    "Percentage",
                    min_value=0.0,
                    max_value=100.0,
                    value=20.0,
                    step=1.0,
                    key=f"evaluation_weight_{subject_index}",
                )

                already_graded = st.checkbox(
                    "I already have this grade",
                    key=f"already_graded_{subject_index}",
                )

                evaluation_grade = None

                if already_graded:

                    evaluation_grade = st.number_input(
                        "Grade",
                        min_value=0.0,
                        max_value=float(grade_scale),
                        value=8.0 if grade_scale == 10 else 80.0,
                        step=0.1,
                        key=f"evaluation_grade_{subject_index}",
                    )

                add_evaluation = st.form_submit_button(
                    "Add evaluation",
                    use_container_width=True,
                )

                if add_evaluation:

                    current_total = sum(
                        item["weight"]
                        for item in subject["evaluations"]
                    )

                    if not evaluation_name.strip():

                        st.warning(
                            "Enter an evaluation name."
                        )

                    elif evaluation_weight <= 0:

                        st.warning(
                            "The percentage must be greater than 0."
                        )

                    elif current_total + evaluation_weight > 100:

                        st.error(
                            "This evaluation would make the total "
                            "percentage exceed 100%."
                        )

                    else:

                        subject["evaluations"].append(
                            {
                                "name": evaluation_name.strip(),
                                "weight": evaluation_weight,
                                "grade": evaluation_grade,
                            }
                        )

                        st.rerun()
