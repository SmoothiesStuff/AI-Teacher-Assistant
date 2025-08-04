import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configure page
st.set_page_config(
    page_title="MindFrame AI Teaching Assistant - Complete Demo",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'assignment_created' not in st.session_state:
    st.session_state.assignment_created = False
if 'assignment_data' not in st.session_state:
    st.session_state.assignment_data = {}
if 'student_dialogue_step' not in st.session_state:
    st.session_state.student_dialogue_step = 0
if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}

# =============================================================================
# DATA GENERATION FUNCTIONS
# =============================================================================

@st.cache_data
def generate_class_data():
    """Generate sample class data for analytics"""
    students = [
        "Jayla Williams", "Jackson Miller", "Olivia Chen", "Marcus Johnson", 
        "Sophia Rodriguez", "Ethan Kim", "Isabella Brown", "Noah Davis",
        "Emma Wilson", "Liam Garcia", "Ava Martinez", "Lucas Anderson"
    ]
    
    # Learning objectives for sample assignment
    objectives = [
        "Analyze primary sources",
        "Identify multiple perspectives", 
        "Evaluate evidence quality",
        "Synthesize information",
        "Draw supported conclusions"
    ]
    
    class_data = []
    for student in students:
        student_data = {
            'student_name': student,
            'objectives_mastered': {obj: random.uniform(0.6, 1.0) for obj in objectives},
            'writing_scores': [random.uniform(6, 10) for _ in range(6)],  # 6 writing samples over time
            'curiosity_paths': random.sample([
                "Climate Change Connections", "Modern Parallels", "Economic Factors",
                "Cultural Impact", "Technology Influence", "Global Perspectives",
                "Environmental Effects", "Social Justice Angles"
            ], random.randint(1, 4)),
            'ai_support_level': random.uniform(0.2, 0.8),  # 20-80% AI assistance
            'total_time_minutes': random.randint(45, 120),
            'questions_asked': random.randint(3, 15),
            'revisions_made': random.randint(2, 8),
            'confusion_areas': random.sample(objectives, random.randint(0, 2))
        }
        class_data.append(student_data)
    
    return class_data, objectives

@st.cache_data 
def generate_individual_student_data(student_name):
    """Generate detailed data for individual student report"""
    objectives = ["Analyze primary sources", "Identify multiple perspectives", 
                 "Evaluate evidence quality", "Synthesize information", "Draw supported conclusions"]
    
    return {
        'name': student_name,
        'objectives_progress': {obj: random.uniform(0.7, 1.0) for obj in objectives},
        'writing_timeline': [
            {'week': f'Week {i+1}', 'score': random.uniform(6.5, 9.5)} 
            for i in range(6)
        ],
        'exploration_tags': random.sample([
            "Economic parallels to 2008", "Environmental justice", "Global perspectives",
            "Technology impacts", "Social movements", "Cultural analysis"
        ], random.randint(2, 4)),
        'ai_breakdown': {
            'student_original': random.uniform(0.4, 0.7),
            'ai_scaffolding': random.uniform(0.2, 0.4), 
            'collaborative': random.uniform(0.1, 0.3)
        }
    }

# =============================================================================
# ASSIGNMENT SETUP TAB
# =============================================================================

def show_assignment_setup():
    st.header("🎯 Create AI-Enhanced Assignment")
    st.markdown("*Design learning experiences where AI amplifies your teaching*")
    
    with st.form("assignment_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Basic assignment info
            st.subheader("📋 Assignment Details")
            title = st.text_input("Assignment Title", 
                                 placeholder="e.g., The Great Depression: Multiple Perspectives")
            
            # Learning objectives
            st.subheader("🎯 Learning Objectives")
            st.markdown("*Select common objectives and add custom ones*")
            
            preset_objectives = st.multiselect(
                "Choose from common objectives:",
                ["Analyze primary sources", "Compare multiple perspectives", "Evaluate evidence quality",
                 "Synthesize information from multiple sources", "Draw evidence-based conclusions",
                 "Identify bias and point of view", "Make historical connections"],
                default=["Analyze primary sources", "Compare multiple perspectives"]
            )
            
            custom_objectives = st.text_area(
                "Add custom objectives (one per line):",
                placeholder="Students will connect historical events to modern issues\nStudents will develop empathy for different viewpoints"
            )
            
            # Resources
            st.subheader("📚 Learning Resources")
            required_resources = st.text_area(
                "Required Resources (URLs or file names):",
                placeholder="https://www.loc.gov/collections/great-depression/\nPrimary_Sources_Packet.pdf\nDocumentary: 'Dust Bowl' (Ken Burns)"
            )
            
            optional_resources = st.text_area(
                "Optional Resources (for curious students):",
                placeholder="https://livinghistory.org/oral-histories\nEconomic_Data_Spreadsheet.xlsx\nComparison: 2008 Financial Crisis"
            )
            
            # AI Configuration
            st.subheader("🤖 AI Assistant Configuration")
            ai_name = st.text_input("AI Assistant Name", value="Professor Explorer")
            
            guidance_level = st.radio(
                "Default AI Guidance Level:",
                ["Minimal - Hints and clarifying questions only",
                 "Moderate - Guided discovery with scaffolding", 
                 "Exploratory - Deep questioning and tangent support"],
                index=1
            )
            
            # Assessment options
            st.subheader("📊 Assessment & Deliverables")
            delivery_formats = st.multiselect(
                "Students can demonstrate learning through:",
                ["Written analysis", "Oral presentation", "Visual timeline", 
                 "Debate participation", "Creative project", "Multimedia story"],
                default=["Written analysis", "Oral presentation"]
            )
        
        with col2:
            st.subheader("✨ Assignment Preview")
            st.markdown("*This is what students will see:*")
            
            preview_box = st.empty()
            
        # Form submission
        submitted = st.form_submit_button("🚀 Create Assignment", use_container_width=True)
        
        if submitted:
            # Combine objectives
            all_objectives = preset_objectives.copy()
            if custom_objectives.strip():
                all_objectives.extend([obj.strip() for obj in custom_objectives.split('\n') if obj.strip()])
            
            # Store assignment data
            st.session_state.assignment_data = {
                'title': title,
                'objectives': all_objectives,
                'required_resources': required_resources.split('\n') if required_resources else [],
                'optional_resources': optional_resources.split('\n') if optional_resources else [],
                'ai_name': ai_name,
                'guidance_level': guidance_level.split(' - ')[0],
                'delivery_formats': delivery_formats
            }
            st.session_state.assignment_created = True
            
            st.success("🎉 Assignment created! Students can now access this through their MindFrame dashboard.")
            st.balloons()
    
    # Show preview
    if st.session_state.assignment_created:
        data = st.session_state.assignment_data
        preview_content = f"""
        ## {data['title']}
        
        **Your AI Learning Partner: {data['ai_name']}**
        *Guidance Style: {data['guidance_level']}*
        
        ### 🎯 What You'll Learn:
        {chr(10).join([f"• {obj}" for obj in data['objectives']])}
        
        ### 📚 Resources to Explore:
        **Required:**{chr(10).join([f"• {res}" for res in data['required_resources'][:3]])}
        
        **For the Curious:**{chr(10).join([f"• {res}" for res in data['optional_resources'][:2]])}
        
        ### 🎨 How You Can Show Your Learning:
        {chr(10).join([f"• {fmt}" for fmt in data['delivery_formats']])}
        
        ---
        *Ready to start? Your AI partner {data['ai_name']} is waiting to explore with you!*
        """
        
        preview_box.markdown(preview_content)

# =============================================================================
# STUDENT EXPERIENCE TAB  
# =============================================================================

def show_student_experience():
    st.header("👩‍🎓 Student Learning Experience")
    st.markdown("*Experience learning through AI partnership*")
    
    # Student selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_student = st.selectbox(
            "Choose a student perspective:",
            ["Jayla Williams", "Jackson Miller", "Olivia Chen"]
        )
        
        if st.button("🔄 Reset Conversation"):
            st.session_state.student_dialogue_step = 0
            st.session_state.student_responses = {}
    
    with col2:
        st.markdown(f"### Learning with Professor Explorer - {selected_student}")
    
    # Dialogue simulation based on step
    dialogue_steps = [
        {
            'type': 'ai_intro',
            'content': f"Hi {selected_student}! I'm Professor Explorer, your AI learning partner. Today we're diving into the causes of the Great Depression. I see you have some great resources to work with. What catches your attention first?",
            'options': ["The photographs of bread lines", "Economic data and graphs", "Personal stories from families"]
        },
        {
            'type': 'content_delivery', 
            'content': "Great choice! Let's start there. I'm going to share some key information in small chunks, and I want you to think out loud as we go. Ready?",
            'info_chunk': "The Great Depression began with the stock market crash of October 1929, but the roots went much deeper. Think of it like a house of cards - multiple factors were already making the economic structure unstable."
        },
        {
            'type': 'comprehension_check',
            'question': "What do you think 'house of cards' means in this context?",
            'options': ["The economy was built on gambling", "The economic system was fragile and interconnected", "People were literally playing cards", "Banks were like card games"]
        },
        {
            'type': 'deeper_exploration',
            'content': "Exactly! The economy was fragile and interconnected. Now, let's explore what made it so unstable. What factors do you think might have contributed?",
            'follow_up': "Think about: How people were buying things, what was happening in agriculture, how banks were operating..."
        },
        {
            'type': 'reflection',
            'content': "You've made some great connections! Now I want you to step back and reflect on your learning process.",
            'prompts': ["What surprised you most?", "What questions do you still have?", "How does this connect to something you already knew?"]
        }
    ]
    
    current_step = st.session_state.student_dialogue_step
    
    if current_step < len(dialogue_steps):
        step = dialogue_steps[current_step]
        
        # AI message
        with st.chat_message("assistant", avatar="🤖"):
            st.write(step['content'])
            
            if 'info_chunk' in step:
                st.info(step['info_chunk'])
        
        # Handle different step types
        if step['type'] == 'ai_intro':
            choice = st.radio("What interests you most?", step['options'], key=f"step_{current_step}")
            if st.button("Tell Professor Explorer", key=f"next_{current_step}"):
                st.session_state.student_responses[current_step] = choice
                st.session_state.student_dialogue_step += 1
                st.rerun()
                
        elif step['type'] == 'content_delivery':
            if st.button("I'm ready to continue!", key=f"next_{current_step}"):
                st.session_state.student_dialogue_step += 1
                st.rerun()
                
        elif step['type'] == 'comprehension_check':
            answer = st.radio("Choose your answer:", step['options'], key=f"step_{current_step}")
            if st.button("Submit Answer", key=f"next_{current_step}"):
                if "fragile and interconnected" in answer:
                    st.success("🎉 Great thinking! You got it!")
                else:
                    st.warning("Hmm, let me help you think about this differently...")
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write("Think about what happens when you remove one card from a house of cards. The whole structure can collapse because everything depends on everything else. How might this apply to an economy?")
                
                st.session_state.student_responses[current_step] = answer
                st.session_state.student_dialogue_step += 1
                st.rerun()
                
        elif step['type'] == 'deeper_exploration':
            student_input = st.text_area("Share your thoughts:", key=f"step_{current_step}")
            if st.button("Share with Professor Explorer", key=f"next_{current_step}"):
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(f"Interesting ideas! I can see you're thinking about {student_input[:50]}... Let's explore that connection further.")
                st.session_state.student_responses[current_step] = student_input
                st.session_state.student_dialogue_step += 1
                st.rerun()
                
        elif step['type'] == 'reflection':
            st.markdown("### 💭 Reflection Time")
            for i, prompt in enumerate(step['prompts']):
                response = st.text_area(prompt, key=f"reflection_{i}")
            
            if st.button("Complete Learning Session", key=f"next_{current_step}"):
                st.success("🌟 Great work! Your teacher will receive a detailed report about your learning journey.")
                with st.expander("See what your teacher learns about your process:"):
                    st.markdown(f"""
                    **{selected_student}'s Learning Journey Report**
                    
                    ✅ **Engagement Level**: High - asked follow-up questions and made connections
                    
                    🎯 **Objectives Progress**:
                    - Analyze primary sources: 85% mastery 
                    - Identify multiple perspectives: 90% mastery
                    - Evaluate evidence quality: 75% mastery
                    
                    💡 **Key Insights**:
                    - Showed strong analytical thinking with "house of cards" metaphor
                    - Made personal connections to family stories
                    - Asked curious questions about modern parallels
                    
                    🔄 **AI Support Used**: 
                    - Scaffolding: 40%
                    - Student original thinking: 60%
                    
                    📝 **Teacher Notes**: {selected_student} demonstrated excellent critical thinking and natural curiosity. Consider enrichment opportunities connecting to modern economics.
                    """)
    else:
        st.success("✨ Learning session complete! Great work exploring the Great Depression causes.")

# =============================================================================
# STUDENT REPORT TAB
# =============================================================================

def show_student_report():
    st.header("📊 Individual Student Report")
    st.markdown("*Deep insights into how each student learns*")
    
    # Student selection
    class_data, objectives = generate_class_data()
    student_names = [student['student_name'] for student in class_data]
    
    selected_student = st.selectbox("Select a student:", student_names)
    
    # Generate individual student data
    student_data = generate_individual_student_data(selected_student)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Learning objectives mastery
        st.subheader("🎯 Learning Objectives Mastery")
        
        obj_df = pd.DataFrame([
            {"Objective": obj, "Mastery": score} 
            for obj, score in student_data['objectives_progress'].items()
        ])
        
        fig_objectives = px.bar(
            obj_df, 
            x='Mastery', 
            y='Objective',
            orientation='h',
            color='Mastery',
            color_continuous_scale='Viridis',
            title=f"{selected_student} - Objective Mastery"
        )
        fig_objectives.update_layout(height=400)
        st.plotly_chart(fig_objectives, use_container_width=True)
        
        # AI Support Breakdown
        st.subheader("🤖 AI Collaboration Breakdown")
        
        ai_data = student_data['ai_breakdown']
        fig_pie = px.pie(
            values=list(ai_data.values()),
            names=['Student Original', 'AI Scaffolding', 'Collaborative'],
            title="Learning Process Composition"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Writing growth timeline
        st.subheader("📈 Writing Growth Timeline")
        
        timeline_df = pd.DataFrame(student_data['writing_timeline'])
        fig_timeline = px.line(
            timeline_df,
            x='week',
            y='score', 
            title="Writing Quality Over Time",
            markers=True
        )
        fig_timeline.update_layout(height=300)
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Exploration tags
        st.subheader("🔍 Curiosity Exploration Paths")
        for tag in student_data['exploration_tags']:
            st.tag(tag)  # This won't work in normal Streamlit, but shows the concept
        
        # Alternative for tags since st.tag doesn't exist
        st.markdown("**Exploration Topics:**")
        for tag in student_data['exploration_tags']:
            st.write(f"🏷️ {tag}")
        
        # Learning insights
        st.subheader("💡 Teacher Insights")
        
        insights = [
            f"✨ **Strength**: Excels at {max(student_data['objectives_progress'], key=student_data['objectives_progress'].get)}",
            f"📈 **Growth**: Writing scores improved {random.randint(15, 35)}% over term",
            f"🎯 **Focus Area**: Could benefit from support in {min(student_data['objectives_progress'], key=student_data['objectives_progress'].get)}",
            f"🚀 **Next Steps**: Ready for advanced work in {random.choice(student_data['exploration_tags'])}"
        ]
        
        for insight in insights:
            st.markdown(insight)

# =============================================================================
# CLASS TRENDS DASHBOARD
# =============================================================================

def show_class_trends():
    st.header("📈 Class Learning Analytics")
    st.markdown("*Understand how your whole class is learning and growing*")
    
    class_data, objectives = generate_class_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mastery distribution
        st.subheader("🎯 Learning Objectives - Class Mastery")
        
        mastery_data = []
        for student in class_data:
            for obj, score in student['objectives_mastered'].items():
                mastery_data.append({
                    'Objective': obj,
                    'Student': student['student_name'], 
                    'Mastery': score
                })
        
        mastery_df = pd.DataFrame(mastery_data)
        
        fig_heatmap = px.box(
            mastery_df,
            x='Objective',
            y='Mastery',
            title="Mastery Score Distribution by Objective"
        )
        fig_heatmap.update_xaxes(tickangle=45)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # AI Support Usage
        st.subheader("🤖 AI Re-teaching Usage")
        
        support_levels = [student['ai_support_level'] for student in class_data]
        support_bins = ['Low (20-40%)', 'Medium (40-60%)', 'High (60-80%)']
        support_counts = [
            sum(1 for x in support_levels if x < 0.4),
            sum(1 for x in support_levels if 0.4 <= x < 0.6), 
            sum(1 for x in support_levels if x >= 0.6)
        ]
        
        fig_pie_support = px.pie(
            values=support_counts,
            names=support_bins,
            title="Distribution of AI Support Usage"
        )
        st.plotly_chart(fig_pie_support, use_container_width=True)
    
    with col2:
        # Confusion zones
        st.subheader("⚠️ Common Confusion Areas")
        
        confusion_counts = {}
        for student in class_data:
            for confusion in student['confusion_areas']:
                confusion_counts[confusion] = confusion_counts.get(confusion, 0) + 1
        
        if confusion_counts:
            confusion_df = pd.DataFrame([
                {'Objective': obj, 'Students_Confused': count}
                for obj, count in confusion_counts.items()
            ])
            
            fig_confusion = px.bar(
                confusion_df,
                x='Students_Confused',
                y='Objective',
                orientation='h',
                title="Number of Students Needing Support by Objective"
            )
            st.plotly_chart(fig_confusion, use_container_width=True)
        
        # Top curiosity paths
        st.subheader("🔥 Top Curiosity Exploration Paths")
        
        all_paths = []
        for student in class_data:
            all_paths.extend(student['curiosity_paths'])
        
        path_counts = {}
        for path in all_paths:
            path_counts[path] = path_counts.get(path, 0) + 1
        
        top_paths = sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for i, (path, count) in enumerate(top_paths, 1):
            st.markdown(f"**{i}. {path}** - {count} students explored")
    
    # Class summary metrics
    st.markdown("---")
    st.subheader("📊 Class Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_mastery = np.mean([np.mean(list(student['objectives_mastered'].values())) for student in class_data])
        st.metric("Average Mastery", f"{avg_mastery:.1%}", "+5% from last assignment")
    
    with col2:
        high_curiosity = sum(1 for student in class_data if len(student['curiosity_paths']) >= 3)
        st.metric("High Curiosity Students", f"{high_curiosity}/12", "🔥 Exploring deeply")
    
    with col3:
        avg_questions = np.mean([student['questions_asked'] for student in class_data])
        st.metric("Avg Questions Asked", f"{avg_questions:.1f}", "📈 Active engagement")
    
    with col4:
        need_support = len([student for student in class_data if student['confusion_areas']])
        st.metric("Students Needing Support", f"{need_support}/12", "👥 Ready for help")

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Header
    st.title("🧠 MindFrame AI Teaching Assistant")
    st.markdown("*Amplifying human teaching through intelligent partnership*")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Assignment Setup", 
        "👩‍🎓 Student Experience", 
        "📊 Student Report",
        "📈 Class Trends"
    ])
    
    with tab1:
        show_assignment_setup()
    
    with tab2:
        show_student_experience()
    
    with tab3:
        show_student_report()
    
    with tab4:
        show_class_trends()
    
    # Footer
    st.markdown("---")
    st.markdown("*This is a demonstration of MindFrame's AI-enhanced learning platform. Real implementation would include secure authentication, privacy controls, and integration with school systems.*")

if __name__ == "__main__":
    main()
