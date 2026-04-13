"""Tab 4 — Talk Tracks for Agent Conversations."""

import streamlit as st


def render():
    st.title('💬 Talk Tracks for Agent Conversations')
    st.markdown(
        '<p style="color:#1a1a1a;font-size:1.05rem;margin-bottom:1.5rem;">'
        'Frameworks for presenting ROI, break-even, and lead channel data to insurance agents.</p>',
        unsafe_allow_html=True,
    )

    # Quick Reference Cards
    st.subheader('Quick Reference: Key Messages')
    qr1, qr2, qr3 = st.columns(3)
    with qr1:
        st.markdown("""
        **ROI Calculator**
        - Focus on *lifetime* value, not just first-year commission
        - A Home policy isn't worth \\$277—it's worth \\$1,387
        - Retention drives revenue
        """)
    with qr2:
        st.markdown("""
        **Break-Even Simulator**
        - Multiple paths to hit your budget
        - Mix matters—optimize your book
        - Find your most efficient policy combination
        """)
    with qr3:
        st.markdown("""
        **Lead Channels**
        - Cost-to-close tells the real story
        - Internet leads cost less per lead, but take more time
        - SF.com leads close faster with fewer touches
        """)

    st.divider()
    st.subheader('Choose Your Approach')

    with st.expander("📊 Data-Driven: Lead with Numbers", expanded=False):
        st.markdown("""
        **Best for:** Analytical agents, high performers, agents who love spreadsheets

        **Opening:**
        > "I ran the numbers on your book. Let me show you something interesting about the lifetime value of your policies."

        **Flow:**
        1. **Show the ROI Calculator** with their actual commission rates
        2. Point out the multiplier effect: "That Home policy you just closed? Over 5 years of renewals, that's not \\$277—it's \\$1,387 in total commission."
        3. **Transition to Break-Even:** "Here's what's cool—I can show you exactly how many policies you need to cover your marketing spend."
        4. **Close with Lead Channels:** "And when we look at cost-to-close, this is how Internet leads vs SF.com stack up for your specific closing rates."

        **Key phrases:**
        - "The math tells us..."
        - "When you run the actual numbers..."
        - "Here's what the data shows..."
        - "This is your specific ROI based on your book"

        **Objection handling:**
        - *"I don't have time for this"* → "This takes 2 minutes. I'll plug in your numbers right now."
        - *"My situation is different"* → "That's exactly why I'm showing you YOUR numbers, not averages."
        """)

    with st.expander("🎯 Goal-Oriented: Focus on Outcomes", expanded=False):
        st.markdown("""
        **Best for:** Struggling agents, agents behind on goals, agents new to marketing

        **Opening:**
        > "You mentioned you need to hit \\$5K/month in new revenue. Let me show you the exact policy mix that gets you there."

        **Flow:**
        1. **Start with Break-Even Simulator:** "What's your monthly marketing budget?" [Plug it in]
        2. Show the combinations: "Look—you could hit your target with 2 Auto + 4 Home, or 1 Auto + 5 Home + 3 Renters. Multiple paths to the same goal."
        3. **Then ROI Calculator:** "And here's why this works—each of these policies is worth more than you think over time."
        4. **Finish with Lead Channels:** "Now let's figure out which lead source gets you there fastest."

        **Key phrases:**
        - "Here's your roadmap..."
        - "This is what it takes to hit your goal..."
        - "You're closer than you think..."
        - "Let's reverse-engineer your target"

        **Objection handling:**
        - *"That seems like a lot of policies"* → "Let's break it down by week. That's just [X] policies per week."
        - *"I've never closed that many"* → "That's why we're looking at multiple combinations—find what's realistic for you."
        """)

    with st.expander("💡 Story-Driven: Use Scenarios", expanded=False):
        st.markdown("""
        **Best for:** Skeptical agents, agents burned by bad marketing, relationship-focused agents

        **Opening:**
        > "I was talking to another agent last week who thought their marketing wasn't working. Want to see what we found?"

        **Flow:**
        1. Tell a story: "They were spending \\$1,000/month and felt like they weren't getting anywhere."
        2. **Show Break-Even:** "We plugged in their numbers and realized they only needed 3 more closed policies per month to break even."
        3. **Show ROI:** "But here's the thing they missed—they were thinking about first-year commission. When you factor in renewals..." [Show the difference]
        4. **Show Lead Channels:** "Then we compared their lead sources and found they were overpaying for one channel by 3x."

        **Key phrases:**
        - "Here's what we discovered..."
        - "The turning point was when we looked at..."
        - "They were surprised to see..."
        - "This changed how they thought about..."

        **Objection handling:**
        - *"That's not me"* → "Right, but the calculator works for any situation. Let's plug in YOUR numbers."
        - *"I don't trust marketing ROI"* → "I get it. That's why I want to show you the actual math, not marketing promises."
        """)

    with st.expander("🚀 Action-Oriented: Get Them Moving", expanded=False):
        st.markdown("""
        **Best for:** Busy agents, agents who avoid analysis, agents who just want to be told what to do

        **Opening:**
        > "Quick question—do you know your cost-to-close on Internet leads vs SF.com?"

        **Flow:**
        1. **Jump straight to Lead Channels:** Show the comparison. "See this difference? That's why we need to optimize your mix."
        2. **Quickly show Break-Even:** "If we hit these numbers [point], you're profitable. That's the target."
        3. **Skip detailed ROI:** Just show grand total. "This is what your book is actually worth when you factor in renewals."
        4. **End with one action:** "Based on this, here's what I recommend you do this week..."

        **Key phrases:**
        - "Bottom line..."
        - "Here's what matters..."
        - "One thing to focus on..."
        - "Action item for this week..."

        **Objection handling:**
        - *"I don't have time"* → "That's why I did the math for you. Just tell me if this looks right [show results]."
        - *"Too complicated"* → "Forget the details. The answer is [X]. Do you want to do it?"
        """)

    st.divider()

    # Common Objections
    st.subheader('Common Objections & Responses')

    with st.expander("💬 'Marketing costs too much'"):
        st.markdown("""
        **What they mean:** "I'm not seeing immediate ROI"

        **Response:** "I hear you. Let's look at your actual numbers in the Break-Even Simulator. [Pull it up] What's your current monthly spend? [Plug in] Okay, so you need [X] policies to break even. Are you hitting that?"

        **If yes:** "Then you're profitable—and here's the thing [switch to ROI Calculator]—every policy after break-even is pure profit, and it compounds over renewals."

        **If no:** "Got it. So we need to either lower your cost-per-lead [Lead Channels tab] or improve your close rate. Which do you want to tackle first?"
        """)

    with st.expander("💬 'Internet leads are junk'"):
        st.markdown("""
        **What they mean:** "I have to work harder for Internet leads"

        **Response:** "Let's test that. Pull up the Lead Channels tab and let's plug in YOUR close rates. What's your closing rate on Internet leads vs SF.com? [Plug in both]"

        **Show the math:** "Okay, so even with a lower close rate, Internet leads cost you [X] to close vs [Y] for SF.com. The question isn't which is better—it's what mix makes sense for your time and budget."

        **Reframe:** "If you're closing 3% on Internet leads, you need 34 quotes to close one. That's a lot of calls. But those calls cost you \\$136 total vs \\$240 for SF.com. So it's really a time-vs-money tradeoff."
        """)

    with st.expander("💬 'I just want more leads'"):
        st.markdown("""
        **What they mean:** "I don't want to think about optimization, just give me volume"

        **Response:** "Fair enough. But before we turn up the volume, let's make sure the math works. [Pull up Break-Even] What's your budget? [Plug in] Okay, at your current close rate, more leads means you need to close [X] policies to stay profitable."

        **Reality check:** "Can you close [X] policies per month? If yes, great—let's increase your budget. If that's a stretch, let's fix your close rate first, THEN scale up."

        **Redirect:** "Because here's the thing—if the math doesn't work at \\$1,000/month, it definitely doesn't work at \\$2,000/month."
        """)

    st.divider()

    # Pro Tips
    st.subheader('Pro Tips for CSMs')
    tip1, tip2 = st.columns(2)
    with tip1:
        st.markdown("""
        **Do's**
        - Always plug in THEIR numbers, not defaults
        - Show one tab at a time—don't overwhelm
        - Use the Export buttons to send them the report
        - Reference specific numbers: "Your Auto policies are worth \\$450 each"
        - End every session with one clear action
        """)
    with tip2:
        st.markdown("""
        **Don'ts**
        - Don't lecture about math—show it
        - Don't use jargon (Pareto, efficiency curves, etc.)
        - Don't show all three tabs if one makes the point
        - Don't let them derail into "marketing doesn't work"
        - Don't forget to export and send them the data
        """)

    st.divider()
    st.info(
        "**💡 Remember:** The calculator isn't the conversation—it's a tool to support YOUR "
        "conversation. Let the agent's questions guide which tab you show and when. "
        "Some calls need all three, some need just one."
    )
