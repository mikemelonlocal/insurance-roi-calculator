"""Tab 5 — How to Use / Tutorial."""

import streamlit as st


def render():
    st.title('📖 How to Use This Calculator')
    st.markdown('Welcome to the Insurance ROI Calculator! This guide will walk you through each feature.')

    st.divider()

    st.subheader('🎯 Quick Overview')
    st.markdown('''
    This tool has **three main calculators** to help you understand insurance agent economics:

    1. **📊 ROI Calculator** - Calculate lifetime commission value from closed policies
    2. **⚖️ Break-Even Simulator** - Find optimal policy mix to hit revenue targets
    3. **🌐 Lead Channels** - Compare cost-effectiveness of different lead sources
    ''')

    st.divider()

    with st.expander('📊 **Tab 1: ROI Calculator** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Calculate the **total lifetime commission** an insurance agent earns from a customer across all their policies.

        ### How to Use
        1. **Select a preset** from the dropdown (Average, Conservative, Moderate, Aggressive, High-Value Client)
        2. **Adjust values** for each insurance product:
           - **Annual Premium** - Yearly cost the customer pays for their policy
           - **Commission %** - Agent's commission rate (typically 10%)
           - **Years as Customer** - Expected policy retention time
           - **Number of Policies** - How many policies the customer has
        3. View the **Summary Table** showing commission breakdown
        4. See the **Revenue Breakdown** chart visualizing total commission by product
        5. Check the **Sensitivity Analysis** to see how retention changes affect the total
        6. **Export** results as HTML, PDF, or Excel to share with agents

        ### Example Scenario
        **"Average New Client"** - A typical household signs up:
        - 1 Auto policy ($2,250/year) x 2 years = **$450 commission**
        - 1 Home policy ($2,775/year) x 5 years = **$1,387.50 commission**
        - 1 Renters policy ($180/year) x 1 year = **$18 commission**
        - **Grand Total: $1,855.50**

        💡 **Pro Tip:** Use the "High-Value Client" preset when discussing ROI with agents who target affluent demographics.
        ''')

    st.divider()

    with st.expander('⚖️ **Tab 2: Break-Even Simulator** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Find the **minimum policy combinations** an agent needs to hit their revenue target.

        ### How to Use
        1. **Set Monthly Budget** - Enter the agent's monthly spend on leads/marketing
        2. **Toggle "Use Tab 1 values"** (on by default) to sync product assumptions
        3. The tool automatically calculates **break-even points** (policies needed to cover budget)
        4. Use **filter dropdowns** to explore specific scenarios
        5. View **Pareto-efficient combinations** (optimal mixes with no wasted effort)
        6. **Export** results for agent coaching or planning sessions

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
        while still meeting the budget. The tool automatically filters out dominated combinations.

        💡 **Pro Tip:** Use this when coaching agents on goal-setting.
        ''')

    st.divider()

    with st.expander('🌐 **Tab 3: Lead Channels** - How It Works', expanded=False):
        st.markdown('''
        ### Purpose
        Compare the **fully-loaded cost** of closing one household from different lead sources.

        ### How to Use
        1. **Set Hourly Wage** - Agent or staff hourly rate
        2. **Configure lead channels** (add or remove channels as needed)
        3. For each channel, set: Cost per Lead, Closing Rate %, Hours per Lead
        4. View **side-by-side comparison** showing total cost to close
        5. **Export** results for budget planning or agent strategy discussions

        ### Understanding the Metrics
        - **Quotes to Close 1 HH** = 100 / Closing Rate %
        - **Lead Cost to Close** = Cost per Lead x Quotes to Close
        - **Payroll to Close** = Hours per Lead x Quotes to Close x Hourly Wage
        - **TOTAL COST TO CLOSE** = Lead Cost + Payroll Cost

        💡 **Pro Tip:** Use the "Add Channel" button to compare 3+ lead sources at once.
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
        - Lower close rates = more payroll cost
        ''')
        st.markdown('''
        **Exporting Data**
        - Use **HTML** for rich formatted reports to share with team
        - Use **PDF** for professional agent-facing documents
        - Use **Excel** to import into spreadsheets for further analysis
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
        **Version 4.0** (April 2026)
        - Modular codebase refactor for maintainability
        - Added sensitivity analysis (retention what-if) to Tab 1
        - Dynamic lead channels (add/remove) in Tab 3
        - Performance-optimized break-even combinations (early termination, iteration cap)
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

        **Calculations:**
        - Break-Even Simulator assumes all leads convert at the same rate
        - Lead Channels assumes consistent time investment per lead
        - Quotes to close are rounded up to nearest integer

        **Technical:**
        - Very large budgets (>$100k) with low premiums may hit the iteration cap
        - Export files must be downloaded individually
        - PDF export requires reportlab package

        If you encounter issues, contact Mike Long.
        ''')

    st.divider()

    st.subheader('📧 Questions or Feedback?')
    st.markdown('''
    This tool was built by **Mike Long** for the Melon Local team.

    Have suggestions for new features? Found a bug?

    **Contact:** Mike Long
    ''')
