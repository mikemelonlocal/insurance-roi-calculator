"""Tab 5 — How to Use / Tutorial."""

import streamlit as st


def render():
    st.title('📖 How to Use This Calculator')
    st.markdown('Welcome to the Insurance ROI Calculator! This guide will walk you through each feature.')

    st.divider()

    st.subheader('🎯 Quick Overview')
    st.markdown('''
    This tool has **three main calculators** plus supporting features:

    1. **💰 Lifetime Value Tracker** - Total lifetime commission, monthly view, cross-sell analysis, scenario comparison
    2. **🎯 Path to Profit** - Break-even combinations with goal tracking
    3. **🔍 Lead Cost Showdown** - Compare lead channels with ROI per channel
    4. **💬 Talk Tracks** - Conversation frameworks for presenting data to agents
    ''')

    st.divider()

    with st.expander('💰 **Tab 1: Lifetime Value Tracker** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Calculate the **total lifetime commission** an insurance agent earns from a customer across all their policies.

        ### How to Use
        1. **Select a preset** from the sidebar dropdown (Average, Conservative, Moderate, Aggressive, High-Value Client)
        2. **Toggle Lifetime / Monthly** view to switch how totals are displayed
        3. **Adjust values** for each insurance product:
           - **Annual Premium** - Yearly cost the customer pays
           - **Commission %** - Agent's commission rate (typically 10%)
           - **Years as Customer** - Expected policy retention time
           - **Number of Policies** - How many the agent has closed
        4. View the **Summary Table** and use the **Copy Total** button to grab the grand total
        5. See the **Revenue Breakdown** chart

        ### New Features
        - **Monthly / Lifetime Toggle** - Switch between seeing totals as lifetime or per-month. Agents think monthly — use this view when talking about recurring income.
        - **Cross-Sell Analysis** - Shows the lifetime value of a household by bundle (Auto only, Home only, Auto + Home, all three). Use this to show agents why cross-selling matters.
        - **Scenario Comparison** - Enter additional policies (e.g. "What if they close 5 more Home policies?") and see the revenue difference side-by-side.
        - **Sensitivity Analysis** - See how the grand total changes when retention shifts by +/- 1 or 2 years.
        - **Agent Name** - Enter the agent's name in the export section to personalize HTML and PDF reports with "Prepared for [Name]".
        - **Copy to Clipboard** - Click "Copy Total" to grab the grand total for quick pasting into emails or Slack.

        ### Example Scenario
        **"Average New Client"** - A typical household signs up:
        - 1 Auto policy ($2,250/year) x 2 years = **$450 commission**
        - 1 Home policy ($2,775/year) x 5 years = **$1,387.50 commission**
        - 1 Renters policy ($180/year) x 1 year = **$18 commission**
        - **Grand Total: $1,855.50**

        💡 **Pro Tip:** Use the Monthly view when agents ask "What does this mean for me each month?" and the Cross-Sell chart when pushing bundled policies.
        ''')

    st.divider()

    with st.expander('🎯 **Tab 2: Path to Profit** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Find the **minimum policy combinations** an agent needs to hit their revenue target.

        ### How to Use
        1. **Set Monthly Budget** - Enter the agent's monthly spend on leads/marketing
        2. **"Use Tab 1 values"** is on by default — product assumptions sync from Tab 1
        3. The tool calculates **single-product break-evens** (policies needed of just one type)
        4. **Goal Tracker** - Enter how many policies the agent has closed this month. Gauge charts show progress toward break-even for each product.
        5. Use **filter dropdowns** to explore specific combinations (e.g. "exactly 3 Home policies")
        6. View **Pareto-efficient combinations** — the smartest paths to hit the goal
        7. **Export** results for agent coaching or planning sessions

        ### New Features
        - **Goal Tracker** - Gauge charts show real-time progress. Enter closed policies this month and see how close the agent is to break-even. Shows remaining revenue needed.
        - **Copy to Clipboard** - Copy the closed revenue total for quick sharing.

        ### Understanding the Results
        - **Total Closed-Won Leads** - Total policies across all products
        - **Total Revenue** - Combined commission from all policies
        - **Above Budget** - How much revenue exceeds the break-even point
        - **Efficiency** - Performance value rating:
          - 🟢 **Break-even** (0-10% over budget) - Most efficient
          - 🟡 **Profitable** (10-30% over) - Better value
          - 🔴 **High-performing** (30%+ over) - Highest value

        ### What is "Pareto-Efficient"?
        A combination is Pareto-efficient if no other combination uses fewer policies in ALL categories
        while still meeting the budget. The tool filters out wasteful combinations automatically.

        💡 **Pro Tip:** During a coaching call, pull up the Goal Tracker and plug in the agent's actual closed count this month. The gauge instantly shows how close they are.
        ''')

    st.divider()

    with st.expander('🔍 **Tab 3: Lead Cost Showdown** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Compare the **fully-loaded cost** of closing one household from different lead sources, and see the **net ROI** per channel.

        ### How to Use
        1. **Set Hourly Wage** - Agent or staff hourly rate
        2. **Configure lead channels** — starts with Internet Leads and SF.com Leads by default
        3. **Add or remove channels** using the buttons (minimum 2, no maximum)
        4. For each channel, set: Channel Name, Cost per Lead, Closing Rate %, Hours per Lead
        5. View the **Cost to Close Comparison** chart and winner callout
        6. Check the **ROI per Channel** section (requires Tab 1 data) to see cost vs. commission earned
        7. Review **Detail Cards** for each channel's full breakdown
        8. **Export** results for budget planning or agent strategy discussions

        ### New Features
        - **Dynamic Channels** - Add as many lead channels as you need (not limited to 2). Compare Internet Leads, SF.com, Google LSA, referrals, etc. side by side.
        - **ROI per Channel** - Combines Tab 3 cost data with Tab 1 commission data to show the net profit per closed household for each channel. A green number means the channel is profitable; red means it costs more to close than the agent earns.
        - **Copy ROI** - Click to copy the net ROI value for any channel.

        ### Understanding the Metrics
        - **Quotes to Close 1 HH** = 100 / Closing Rate %
        - **Lead Cost to Close** = Cost per Lead x Quotes to Close
        - **Payroll to Close** = Hours per Lead x Quotes to Close x Hourly Wage
        - **TOTAL COST TO CLOSE** = Lead Cost + Payroll Cost
        - **Net ROI** = Average Commission Earned - Total Cost to Close

        💡 **Pro Tip:** When an agent says "Internet leads are junk," add their actual close rates and show the ROI comparison. The math usually tells a different story.
        ''')

    st.divider()

    st.subheader('💡 Tips & Best Practices')
    col_tip1, col_tip2 = st.columns(2)
    with col_tip1:
        st.markdown('''
        **Using Presets**
        - Start with "Average" for typical client scenarios
        - Use "Conservative" for worst-case planning
        - Use "Aggressive" for stretch goals
        - Customize values after selecting a preset
        ''')
        st.markdown('''
        **Break-Even Filtering**
        - Select "Any" to see all efficient combinations
        - Pick specific counts to answer agent questions
        - Look for "Break-even" efficiency to minimize wasted budget
        ''')
    with col_tip2:
        st.markdown('''
        **Lead Channel Comparison**
        - Don't just compare cost-per-lead
        - Factor in closing rate AND time investment
        - Check the ROI section to see if a channel is actually profitable
        - Add custom channels for referrals, events, etc.
        ''')
        st.markdown('''
        **Sharing & Exporting**
        - Use **HTML** for rich formatted reports to share with team
        - Use **PDF** for professional agent-facing documents
        - Use **Excel** to import into spreadsheets for further analysis
        - Use **Batch ZIP** (bottom of page) to download all reports at once
        - **Generate Share Link** in the sidebar to create a URL with your current inputs
        - Add the **Agent Name** field to personalize exports with "Prepared for [Name]"
        ''')

    st.divider()

    # Data Sources
    st.subheader('📚 Data Sources')
    st.markdown('The default premium values are based on 2026 U.S. national averages from multiple industry sources:')

    with st.expander('🚗 Auto Insurance - $2,250/year average'):
        st.markdown('''
        1. **The Zebra** - "2026 State of Insurance Auto Trend Report" (January 29, 2026)
        2. **Experian** - "Average Cost of Car Insurance in the US for 2026" (February 13, 2026)
        3. **U.S. News** - "Average Cost of Car Insurance in the U.S. for 2026" (February 24, 2026)
        4. **Insurance Journal** - "After Falling 6% in 2025, Average Auto Insurance Cost Will Stabilize in 2026" (February 3, 2026)
        5. **Beinsure** - "US Auto Insurance Rates by States in 2026" (January 1, 2026)
        ''')

    with st.expander('🏠 Home Insurance - $2,775/year average'):
        st.markdown('''
        1. **NerdWallet** - "How Much Is Homeowners Insurance? Average 2026 Rates" (March 2026)
        2. **Insurance.com** - "Average homeowners insurance rates by state in 2026" (March 20, 2026)
        3. **Insurance Journal** - "US Home Insurance Prices Set to Keep Rising With Severe Weather" (March 18, 2026)
        4. **Matic** - "2026 Home Insurance Trends & Predictions" (December 19, 2025)
        ''')

    with st.expander('🏢 Renters Insurance - $180/year average'):
        st.markdown('''
        1. **NerdWallet** - "How Much Is Renters Insurance in 2026?" (March 2026)
        2. **The Hartford** - "Renters Insurance Cost" (September 8, 2025)
        3. **MoneyGeek** - "Average Cost of Renters Insurance in 2026" (March 2026)
        4. **Insurance.com** - "How much is renters insurance in 2026?" (March 25, 2026)
        5. **SoFi** - "How Much Is Renters Insurance 2026?" (March 2026)
        ''')

    st.markdown(
        '*Note: These averages represent national figures and may vary significantly by state, '
        'demographics, and coverage levels.*'
    )

    st.divider()

    st.subheader('📋 Version History & Known Limitations')

    with st.expander('Version History'):
        st.markdown('''
        **Version 4.1** (April 2026)
        - Monthly / Lifetime view toggle in Tab 1
        - Cross-sell analysis showing household value by bundle
        - Scenario comparison ("What if they close 5 more?")
        - Goal tracker with gauge charts in Tab 2
        - ROI per channel in Tab 3 (cost vs. commission earned)
        - Dynamic lead channels (add/remove N channels)
        - Copy-to-clipboard buttons for key numbers
        - Agent name field for personalized exports
        - URL query params for shareable scenarios
        - Batch ZIP export (all tabs in one download)
        - Forced light theme for consistent branding

        **Version 4.0** (April 2026)
        - Modular codebase refactor for maintainability
        - Added sensitivity analysis (retention what-if) to Tab 1
        - Performance-optimized break-even combinations
        - Improved Pareto filtering algorithm
        - Tab 1 values sync to Tab 2 by default
        - Added caching for export generation
        - Integer policy count inputs

        **Version 3.0** (March 30, 2026)
        - Added Tutorial tab with step-by-step guides
        - Added Data Sources section with proper citations
        - Implemented "Clear Filters" and "Reset to Defaults" buttons
        - Added validation warnings for unrealistic values
        - Changed terminology to "closed-won leads"
        - PDF export now available on all three tabs

        **Version 2.0** (March 2026)
        - Added Pareto-efficient filtering in Break-Even Simulator
        - Implemented HTML, PDF, and CSV export options
        - Added preset scenarios

        **Version 1.0** (Initial Release)
        - Three core calculators: ROI, Break-Even, Lead Channels
        ''')

    with st.expander('Known Limitations'):
        st.markdown('''
        **Data & Assumptions:**
        - Premium values are national averages
        - Does not account for policy cancellations or mid-term adjustments
        - ROI per channel uses a simple average across all product commissions

        **Calculations:**
        - Break-Even Simulator assumes all leads convert at the same rate
        - Lead Channels assumes consistent time investment per lead
        - Quotes to close are rounded up to nearest integer

        **Technical:**
        - Very large budgets (>$100k) with low premiums may hit the iteration cap
        - Batch ZIP includes Tab 1 reports only (Tab 2/3 exports are available individually)
        - PDF export requires reportlab package
        - Copy-to-clipboard requires HTTPS (works on Streamlit Cloud, may not work on localhost HTTP)
        - Share links encode Tab 1 values only

        If you encounter issues, contact Mike Long.
        ''')

    st.divider()

    st.subheader('📧 Questions or Feedback?')
    st.markdown('''
    This tool was built by **Mike Long** for the Melon Local team.

    Have suggestions for new features? Found a bug?

    **Contact:** Mike Long
    ''')
