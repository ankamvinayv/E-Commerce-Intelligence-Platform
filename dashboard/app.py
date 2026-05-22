import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

# ── page config ──────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── problem statements data ───────────────────────────────
PROBLEMS = [
    {
        "id": "P1",
        "pillar": "🎯 Customer Experience",
        "color": "#FAECE7",
        "border": "#D85A30",
        "icon": "👗",
        "title": "Fashion products look different in reality",
        "problem": "Customers order clothes or accessories online based on product photos, but when the item arrives it looks completely different — wrong colour, different fabric, or misleading size.",
        "impact": "High return rates, customer frustration, loss of trust in the platform.",
        "how_we_solved": "We analysed return reasons data and found that 'colour mismatch' and 'not as shown' together account for a significant share of all returns — directly proving this is a real, measurable problem.",
        "solution": "Flag listings with high visual-mismatch return rates and recommend sellers improve photo accuracy."
    },
    {
        "id": "P2",
        "pillar": "🎯 Customer Experience",
        "color": "#FAECE7",
        "border": "#D85A30",
        "icon": "🔍",
        "title": "Beauty buyers can't verify product authenticity",
        "problem": "When buying beauty or skincare products online, customers have no easy way to tell if a product is genuine or counterfeit. Fake products can cause skin damage or health risks.",
        "impact": "Health risks for customers, brand damage for sellers, loss of consumer confidence.",
        "how_we_solved": "We built an Isolation Forest ML model that scores every seller based on their fake product rate, complaint history, and unusual pricing patterns — automatically flagging suspicious sellers.",
        "solution": "Sellers with high anomaly scores are flagged for review before their listings go live."
    },
    {
        "id": "P3",
        "pillar": "🎯 Customer Experience",
        "color": "#FAECE7",
        "border": "#D85A30",
        "icon": "📦",
        "title": "Small orders arrive in oversized, wasteful packaging",
        "problem": "A customer orders a small item like a pen or a bottle of nail polish, and it arrives in a box big enough for a microwave — filled with bubble wrap and paper. This wastes materials and frustrates eco-conscious buyers.",
        "impact": "Higher shipping costs, unnecessary environmental waste, poor unboxing experience.",
        "how_we_solved": "We cross-matched product dimensions with the actual box sizes used for shipping and calculated an over-packaging rate for every product category.",
        "solution": "Identify the worst offending categories and implement smart box-size assignment rules."
    },
    {
        "id": "P4",
        "pillar": "🎯 Customer Experience",
        "color": "#FAECE7",
        "border": "#D85A30",
        "icon": "🕐",
        "title": "Working professionals can't return products outside business hours",
        "problem": "Most courier pickup services for returns only operate 9am–6pm on weekdays. But working professionals are at the office during these exact hours — making it nearly impossible to hand over a return package.",
        "impact": "Customers give up on returns, leading to frustration and reduced trust in the platform.",
        "how_we_solved": "We analysed every return attempt by hour of day and found that a large percentage of customers try to initiate returns in the evening or early morning — outside standard business hours.",
        "solution": "Extend return pickup windows to evenings and weekends, or offer drop-off point options."
    },
    {
        "id": "P5",
        "pillar": "🚚 Supply Chain",
        "color": "#E6F1FB",
        "border": "#378ADD",
        "icon": "🏪",
        "title": "Shoppers visit stores only to find items unavailable",
        "problem": "A customer sees a product listed as available online, travels to pick it up or waits for delivery, only to find out it's out of stock. The website didn't reflect the real inventory.",
        "impact": "Wasted trips, cancelled orders, damage to brand reputation.",
        "how_we_solved": "We built an XGBoost machine learning model trained on historical stock levels, reorder points, and demand patterns. It predicts which products are likely to run out of stock before it actually happens.",
        "solution": "Products with a high stockout risk score get automatic restock alerts sent to warehouse teams."
    },
    {
        "id": "P6",
        "pillar": "🚚 Supply Chain",
        "color": "#E6F1FB",
        "border": "#378ADD",
        "icon": "🍎",
        "title": "Quick-delivery apps send bruised fruits and vegetables",
        "problem": "Customers ordering fresh produce or perishable food items through quick-delivery apps often receive items that are bruised, wilted, or near-expiry — despite paying for fast delivery.",
        "impact": "Food waste, customer refund requests, negative reviews for the platform.",
        "how_we_solved": "We correlated quality complaint data with delivery transit times and found that perishable items with transit times over 48 hours have a dramatically higher complaint rate than those delivered quickly.",
        "solution": "Route perishable items through faster delivery channels and flag temperature-sensitive orders."
    },
    {
        "id": "P7",
        "pillar": "🚚 Supply Chain",
        "color": "#E6F1FB",
        "border": "#378ADD",
        "icon": "🗺️",
        "title": "Rural residents can't receive doorstep deliveries",
        "problem": "People living in rural or semi-urban areas place orders online just like city dwellers, but a large percentage of their deliveries fail — couriers either can't find the address or don't service the pincode at all.",
        "impact": "Rural customers are excluded from e-commerce, widening the urban-rural access gap.",
        "how_we_solved": "We mapped delivery success rates by pincode and found a significant gap between urban and rural delivery success rates — with rural zones failing far more often.",
        "solution": "Build hub-and-spoke models with local delivery agents for rural pincodes showing high failure rates."
    },
    {
        "id": "P8",
        "pillar": "💰 Pricing & Access",
        "color": "#E1F5EE",
        "border": "#1D9E75",
        "icon": "💸",
        "title": "Hidden shipping fees inflate affordable product prices",
        "problem": "A customer adds a ₹199 product to their cart, but at checkout discovers ₹99 in shipping and handling fees they didn't know about. Many abandon the cart right at this moment.",
        "impact": "High cart abandonment rates, loss of completed sales, customer distrust.",
        "how_we_solved": "We compared cart abandonment rates for orders with and without hidden fees and found a clear, measurable jump in abandonment when a hidden fee is revealed at checkout.",
        "solution": "Show all fees upfront on the product page. Our data shows this directly reduces abandonment."
    },
    {
        "id": "P9",
        "pillar": "💰 Pricing & Access",
        "color": "#E1F5EE",
        "border": "#1D9E75",
        "icon": "🤝",
        "title": "Online platforms don't enable price negotiation or bulk discounts",
        "problem": "Small business owners or bulk buyers who want to purchase 20 units of a product have no way to negotiate a better price online — they pay the same per-unit price as someone buying just one.",
        "impact": "Lost bulk sale opportunities, buyers going to wholesalers offline instead.",
        "how_we_solved": "We calculated price elasticity per product category — measuring how much order quantity increases when price drops. Categories with high elasticity are the best candidates for bulk discount tiers.",
        "solution": "Introduce tiered pricing: buy 5+ units and get 10% off, buy 10+ and get 20% off. Our simulator shows the revenue impact."
    },
    {
        "id": "P10",
        "pillar": "💰 Pricing & Access",
        "color": "#E1F5EE",
        "border": "#1D9E75",
        "icon": "🏠",
        "title": "Large families can't access wholesale grocery pricing online",
        "problem": "A family of 6 buying groceries for the month needs to purchase in bulk — but online grocery platforms only offer retail pricing. Offline wholesale markets like Metro Cash & Carry serve them, but not online.",
        "impact": "Large families overpay for groceries online and prefer offline bulk stores.",
        "how_we_solved": "We segmented customers by household size and found that families of 5 or more consistently place higher-value orders — proving there's a wholesale-ready customer segment already on the platform.",
        "solution": "Create a 'Family Pack' tier with wholesale pricing for household sizes of 4+ members."
    }
]

# ── load data ─────────────────────────────────────────────
BASE = os.path.dirname(__file__)

@st.cache_data
def load_data():
    orders     = pd.read_csv(os.path.join(BASE, 'orders.csv'),    parse_dates=['order_date'])
    products   = pd.read_csv(os.path.join(BASE, 'products.csv'))
    customers  = pd.read_csv(os.path.join(BASE, 'customers.csv'))
    returns    = pd.read_csv(os.path.join(BASE, 'returns.csv'))
    deliveries = pd.read_csv(os.path.join(BASE, 'deliveries.csv'))
    stockout   = pd.read_csv(os.path.join(BASE, 'stockout_risk_scores.csv'))
    sellers    = pd.read_csv(os.path.join(BASE, 'seller_risk_scores.csv'))
    elasticity = pd.read_csv(os.path.join(BASE, 'category_elasticity.csv'))
    return orders, products, customers, returns, deliveries, stockout, sellers, elasticity

orders, products, customers, returns_df, deliveries, stockout, sellers, elasticity = load_data()

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 E-Commerce Analytics")
    st.markdown("**Startup Problem-Solving Dashboard**")
    st.markdown("---")

    # ── PROBLEM STATEMENTS EXPANDER ──
    st.markdown("### 📋 The 10 Problems We Solve")
    st.markdown(
        "<span style='font-size:12px;color:gray'>"
        "Click any problem below to read what it is, "
        "why it matters, and how data solves it."
        "</span>", unsafe_allow_html=True
    )
    st.markdown("")

    pillar_icons = {
        "🎯 Customer Experience": "#FAECE7",
        "🚚 Supply Chain": "#E6F1FB",
        "💰 Pricing & Access": "#E1F5EE"
    }

    for pillar in pillar_icons:
        pillar_problems = [p for p in PROBLEMS if p["pillar"] == pillar]
        st.markdown(f"**{pillar}**")
        for p in pillar_problems:
            with st.expander(f"{p['icon']} {p['id']} — {p['title']}"):
                st.markdown(
                    f"<div style='"
                    f"background:{p['color']};"
                    f"border-left: 3px solid {p['border']};"
                    f"border-radius:6px;"
                    f"padding:10px 14px;"
                    f"margin-bottom:8px"
                    f"'>"
                    f"<strong>🔴 The Problem</strong><br>"
                    f"<span style='font-size:13px'>{p['problem']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='"
                    f"background:#FFF8E7;"
                    f"border-left: 3px solid #F5A623;"
                    f"border-radius:6px;"
                    f"padding:10px 14px;"
                    f"margin-bottom:8px"
                    f"'>"
                    f"<strong>⚠️ Business Impact</strong><br>"
                    f"<span style='font-size:13px'>{p['impact']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='"
                    f"background:#E8F8F3;"
                    f"border-left: 3px solid #1D9E75;"
                    f"border-radius:6px;"
                    f"padding:10px 14px;"
                    f"margin-bottom:8px"
                    f"'>"
                    f"<strong>📊 How We Used Data</strong><br>"
                    f"<span style='font-size:13px'>{p['how_we_solved']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='"
                    f"background:#EEF2FF;"
                    f"border-left: 3px solid #7F77DD;"
                    f"border-radius:6px;"
                    f"padding:10px 14px"
                    f"'>"
                    f"<strong>✅ Recommended Solution</strong><br>"
                    f"<span style='font-size:13px'>{p['solution']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        st.markdown("")

    st.markdown("---")
    st.markdown("**Stack:** Python · Pandas · XGBoost · Plotly · Streamlit")

# ── header ────────────────────────────────────────────────
st.title("🛒 E-Commerce Intelligence Platform")
st.markdown("*Solving 10 real-world business problems across Supply Chain, Pricing & Customer Trust*")

# ── inline problem overview (collapsible) ─────────────────
with st.expander("ℹ️  What does this dashboard solve? Click to see all 10 problems at a glance"):
    cols = st.columns(3)
    for i, p in enumerate(PROBLEMS):
        with cols[i % 3]:
            st.markdown(
                f"<div style='"
                f"background:{p['color']};"
                f"border:1px solid {p['border']};"
                f"border-radius:8px;"
                f"padding:10px 12px;"
                f"margin-bottom:8px;"
                f"min-height:100px"
                f"'>"
                f"<div style='font-size:11px;font-weight:600;color:{p['border']};margin-bottom:4px'>"
                f"{p['id']} · {p['pillar']}</div>"
                f"<div style='font-size:13px;font-weight:500;margin-bottom:4px'>"
                f"{p['icon']} {p['title']}</div>"
                f"<div style='font-size:11px;color:#555;line-height:1.5'>"
                f"{p['problem'][:100]}...</div>"
                f"</div>",
                unsafe_allow_html=True
            )

st.markdown("---")

# ── top KPI row ───────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
total_orders      = len(orders)
total_returns     = len(returns_df)
return_rate       = total_returns / total_orders * 100
rural_gap         = (deliveries[deliveries['is_rural']==False]['delivery_success'].mean() -
                     deliveries[deliveries['is_rural']==True]['delivery_success'].mean()) * 100
fee_abandon       = (orders[orders['hidden_fee']>0]['cart_abandoned'].mean() -
                     orders[orders['hidden_fee']==0]['cart_abandoned'].mean()) * 100
high_risk_sellers = (sellers['is_suspicious'] == True).sum()

col1.metric("Total Orders",         f"{total_orders:,}")
col2.metric("Return Rate",          f"{return_rate:.1f}%",    delta=f"-{return_rate:.1f}% target 0")
col3.metric("Rural Delivery Gap",   f"{rural_gap:.1f}%",      delta=f"-{rural_gap:.1f}% vs urban",   delta_color="inverse")
col4.metric("Fee Abandonment Lift", f"+{fee_abandon:.1f}%",   delta="hidden fee impact",             delta_color="inverse")
col5.metric("Suspicious Sellers",   f"{high_risk_sellers}",   delta="flagged by AI",                 delta_color="inverse")

st.markdown("---")

# ── tabs ──────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📦  Operations & Stockout",
    "💰  Pricing & Discounts",
    "🔍  Seller Trust"
])

# ════════════════════════════════════════════════════════
# TAB 1 — OPERATIONS
# ════════════════════════════════════════════════════════
with tab1:
    st.subheader("📦 Inventory & Stockout Risk")

    # plain-english explainer
    st.info(
        "**What you're looking at:** Our AI model scanned every product and assigned a "
        "stockout risk score from 0 to 1. A score above 0.6 means the product is very "
        "likely to run out of stock soon. Use the filters below to find which categories "
        "and products need urgent restocking."
    )

    col_a, col_b = st.columns([1, 2])
    with col_a:
        risk_filter = st.selectbox("Filter by risk level", ["All", "High", "Medium", "Low"])
        cat_filter  = st.multiselect("Filter by category",
                                      options=stockout['category'].unique().tolist(),
                                      default=stockout['category'].unique().tolist())

    filtered = stockout[stockout['category'].isin(cat_filter)]
    if risk_filter != "All":
        filtered = filtered[filtered['risk_label'] == risk_filter]

    with col_b:
        risk_counts = stockout.groupby(['category','risk_label']).size().reset_index(name='count')
        fig_risk = px.bar(risk_counts, x='category', y='count', color='risk_label',
                          color_discrete_map={'High':'#D85A30','Medium':'#F5A623','Low':'#1D9E75'},
                          title='How many products in each risk level, by category?',
                          labels={'count':'Number of products','category':'Category'})
        fig_risk.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                               legend_title='Risk Level', height=320)
        st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown(f"**Showing {len(filtered)} products** — sorted by highest risk first")
    st.dataframe(
        filtered[['product_id','category','stock_level','stockout_risk_score','risk_label']]
                  .sort_values('stockout_risk_score', ascending=False)
                  .head(20)
                  .style.background_gradient(subset=['stockout_risk_score'], cmap='RdYlGn_r'),
        use_container_width=True, height=320
    )

    st.markdown("---")
    st.subheader("🚚 Delivery Performance")
    st.info(
        "**What you're looking at:** Two charts showing delivery problems. "
        "Left: how often deliveries succeed in cities vs villages. "
        "Right: how product quality complaints rise the longer a delivery takes — "
        "especially for fresh food and perishables."
    )

    col_c, col_d = st.columns(2)
    with col_c:
        rural_data = deliveries.groupby('is_rural')['delivery_success'].mean().reset_index()
        rural_data['zone'] = rural_data['is_rural'].map({True:'Rural', False:'Urban'})
        rural_data['success_pct'] = rural_data['delivery_success'] * 100
        fig_rural = px.bar(rural_data, x='zone', y='success_pct',
                           color='zone',
                           color_discrete_map={'Urban':'#378ADD','Rural':'#D85A30'},
                           title='Delivery Success: City vs Village (P7)',
                           labels={'success_pct':'Orders successfully delivered (%)','zone':''},
                           text='success_pct')
        fig_rural.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_rural.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                showlegend=False, height=360)
        st.plotly_chart(fig_rural, use_container_width=True)

    with col_d:
        del_prod = deliveries.merge(orders[['order_id','product_id']], on='order_id', how='left')
        del_prod = del_prod.merge(products[['product_id','is_perishable']], on='product_id', how='left')
        del_prod['transit_bucket'] = pd.cut(del_prod['transit_hours'],
                                             bins=[0,12,24,48,96],
                                             labels=['Under 12h','12–24h','24–48h','48–96h'])
        complaint_r = (del_prod.groupby(['transit_bucket','is_perishable'])['quality_complaint']
                       .mean().reset_index())
        complaint_r['type'] = complaint_r['is_perishable'].map({True:'Fresh/Perishable',False:'Regular products'})
        complaint_r['complaint_pct'] = complaint_r['quality_complaint'] * 100
        fig_perish = px.bar(complaint_r, x='transit_bucket', y='complaint_pct', color='type',
                            barmode='group',
                            color_discrete_map={'Fresh/Perishable':'#D85A30','Regular products':'#378ADD'},
                            title='Complaint rate rises with delivery time (P6)',
                            labels={'complaint_pct':'% of deliveries with complaints',
                                    'transit_bucket':'How long the delivery took'})
        fig_perish.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=360)
        st.plotly_chart(fig_perish, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 2 — PRICING
# ════════════════════════════════════════════════════════
with tab2:
    st.subheader("💰 Pricing Transparency & Discounts")
    st.info(
        "**What you're looking at:** Three pricing insights. "
        "First — proof that hidden fees cause customers to abandon their cart. "
        "Second — which product categories respond best to price drops (elasticity). "
        "Third — an interactive simulator where you can test what happens to revenue "
        "when you offer a bulk discount."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fee_data = orders.groupby(orders['hidden_fee'] > 0)['cart_abandoned'].mean().reset_index()
        fee_data.columns = ['has_fee','abandon_rate']
        fee_data['label'] = fee_data['has_fee'].map({True:'Hidden fee added at checkout',
                                                      False:'Price shown upfront, no surprises'})
        fee_data['abandon_pct'] = fee_data['abandon_rate'] * 100
        fig_fee = px.bar(fee_data, x='label', y='abandon_pct',
                         color='label',
                         color_discrete_map={
                             'Hidden fee added at checkout':'#D85A30',
                             'Price shown upfront, no surprises':'#1D9E75'
                         },
                         title='Do hidden fees make customers abandon their cart? (P8)',
                         labels={'abandon_pct':'% of customers who abandoned cart','label':''},
                         text='abandon_pct')
        fig_fee.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_fee.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              showlegend=False, height=360)
        st.plotly_chart(fig_fee, use_container_width=True)

    with col_b:
        fig_elast = px.bar(
            elasticity.sort_values('elasticity'),
            x='elasticity', y='category', orientation='h',
            color='elasticity',
            color_continuous_scale=['#D85A30','#F5A623','#1D9E75'],
            title='Which categories sell more when price drops? (P9)',
            labels={'elasticity':'Price sensitivity score (more negative = more sensitive)',
                    'category':'Product category'}
        )
        fig_elast.add_vline(x=0, line_dash='dash', line_color='gray', opacity=0.5)
        fig_elast.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                coloraxis_showscale=False, height=360)
        st.plotly_chart(fig_elast, use_container_width=True)

    st.markdown("---")
    st.subheader("🧮 Bulk Discount Revenue Simulator")
    st.markdown(
        "**Try it yourself:** Adjust the sliders below to simulate what happens to revenue "
        "when you offer a discount for bulk orders. The model uses real price sensitivity "
        "data to estimate how many more units customers will order."
    )

    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        sim_category   = st.selectbox("Product category", elasticity['category'].tolist())
        sim_base_price = st.slider("Product price (₹)", 100, 5000, 500, 50)
    with sim_col2:
        sim_discount   = st.slider("Discount you want to offer (%)", 0, 40, 10, 5)
        sim_min_qty    = st.slider("Minimum units to qualify for discount", 1, 20, 3)
    with sim_col3:
        sim_customers  = st.slider("How many customers are eligible?", 100, 5000, 1000, 100)

    elast_val        = elasticity[elasticity['category'] == sim_category]['elasticity'].values[0]
    price_change_pct = -sim_discount / 100
    qty_change_pct   = elast_val * price_change_pct
    new_avg_qty      = max(sim_min_qty, sim_min_qty * (1 + qty_change_pct))
    discounted_price = sim_base_price * (1 - sim_discount / 100)
    base_revenue     = sim_base_price * sim_min_qty * sim_customers
    new_revenue      = discounted_price * new_avg_qty * sim_customers
    revenue_delta    = new_revenue - base_revenue

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Price sensitivity",    f"{elast_val:+.2f}",
              help="How much quantity changes for every 1% price change")
    r2.metric("New discounted price", f"₹{discounted_price:,.0f}", f"-{sim_discount}%")
    r3.metric("Expected avg qty",     f"{new_avg_qty:.1f} units",
              f"+{qty_change_pct*100:.1f}% more units")
    r4.metric("Revenue impact",
              f"₹{new_revenue:,.0f}",
              f"{'+'if revenue_delta>=0 else ''}{revenue_delta:,.0f} vs no discount",
              delta_color="normal" if revenue_delta >= 0 else "inverse")

    if revenue_delta >= 0:
        st.success(
            f"✅ Offering a **{sim_discount}% discount** on **{sim_category}** for orders of "
            f"**{sim_min_qty}+ units** is expected to **increase revenue by ₹{revenue_delta:,.0f}** "
            f"because customers in this category are price-sensitive and will buy more when prices drop."
        )
    else:
        st.warning(
            f"⚠️ A **{sim_discount}% discount** on **{sim_category}** may reduce revenue by "
            f"₹{abs(revenue_delta):,.0f} because this category is not very price-sensitive. "
            f"Try a smaller discount or a different category."
        )

    st.markdown("---")
    st.subheader("🏠 Do larger families spend more? (P10)")
    st.markdown(
        "This chart shows average order value grouped by household size. "
        "If larger families consistently spend more, they are strong candidates "
        "for a wholesale pricing tier."
    )
    orders_c = orders.merge(customers[['customer_id','household_size']], on='customer_id', how='left')
    hh_aov   = orders_c.groupby('household_size')['final_price'].mean().reset_index()
    hh_aov.columns = ['household_size','avg_order_value']
    fig_hh = px.line(hh_aov, x='household_size', y='avg_order_value', markers=True,
                     title='Average order value by household size — wholesale opportunity (P10)',
                     labels={'avg_order_value':'Average order value (₹)',
                             'household_size':'Number of people in the household'})
    fig_hh.update_traces(line_color='#1D9E75', marker_color='#085041', marker_size=9)
    fig_hh.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=340)
    st.plotly_chart(fig_hh, use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 3 — SELLER TRUST
# ════════════════════════════════════════════════════════
with tab3:
    st.subheader("🔍 Seller Authenticity & Trust")
    st.info(
        "**What you're looking at:** Our AI model (Isolation Forest) analysed every seller's "
        "behaviour — how many fake products they list, how many counterfeit complaints they receive, "
        "and unusual pricing patterns. Sellers that behave very differently from normal are "
        "automatically flagged as suspicious. No human review needed to find the bad actors."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fig_scatter = px.scatter(
            sellers,
            x='fake_product_rate',
            y='complaint_rate',
            color='is_suspicious',
            color_discrete_map={True:'#D85A30', False:'#378ADD'},
            size='total_products',
            hover_data=['seller_id','counterfeit_complaints','anomaly_score'],
            title='Suspicious sellers cluster in the top-right corner (P2)',
            labels={
                'fake_product_rate': 'What % of their products are fake',
                'complaint_rate': 'Complaints received per product listed',
                'is_suspicious': 'Flagged by AI'
            }
        )
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_b:
        tier_counts = sellers['risk_tier'].value_counts().reset_index()
        tier_counts.columns = ['risk_tier','count']
        fig_tier = px.pie(
            tier_counts, names='risk_tier', values='count',
            color='risk_tier',
            color_discrete_map={'Low Risk':'#1D9E75','Medium Risk':'#F5A623','High Risk':'#D85A30'},
            title='How are sellers distributed across risk tiers?',
            hole=0.45
        )
        fig_tier.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig_tier, use_container_width=True)

    st.markdown("---")
    st.subheader("🚨 Sellers That Need Attention")
    st.markdown(
        "The table below shows sellers flagged by the AI model. "
        "A higher **anomaly score** means more suspicious behaviour. "
        "Platform teams should review High Risk sellers before allowing new listings."
    )

    show_all = st.checkbox("Show all sellers (uncheck = suspicious only)", value=False)
    display_sellers = sellers if show_all else sellers[sellers['is_suspicious'] == True]

    st.dataframe(
        display_sellers[[
            'seller_id','total_products','fake_product_rate',
            'counterfeit_complaints','complaint_rate',
            'anomaly_score','risk_tier','is_suspicious'
        ]].sort_values('anomaly_score', ascending=False)
          .rename(columns={
              'seller_id': 'Seller ID',
              'total_products': 'Products Listed',
              'fake_product_rate': 'Fake Product Rate',
              'counterfeit_complaints': 'Counterfeit Complaints',
              'complaint_rate': 'Complaints Per Product',
              'anomaly_score': 'AI Risk Score',
              'risk_tier': 'Risk Tier',
              'is_suspicious': 'Flagged?'
          })
          .style.background_gradient(subset=['AI Risk Score'], cmap='RdYlGn_r'),
        use_container_width=True, height=360
    )

    csv = display_sellers.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download seller risk report as spreadsheet",
        data=csv,
        file_name='seller_risk_report.csv',
        mime='text/csv'
    )

    st.markdown("---")
    st.subheader("📦 Are products being shipped in the right box size? (P3)")
    st.markdown(
        "This chart shows what percentage of products in each category are shipped "
        "in a box that is larger than they actually need. Higher = more waste."
    )
    size_map = {'S':1,'M':2,'L':3,'XL':4}
    products['box_score']    = products['box_size_used'].map(size_map)
    products['needed_score'] = products['actual_size_needed'].map(size_map)
    products['overpackaged'] = products['box_score'] > products['needed_score']
    waste_cat = products.groupby('category')['overpackaged'].mean().reset_index()
    waste_cat.columns = ['category','overpackaged_rate']
    waste_cat['overpackaged_pct'] = waste_cat['overpackaged_rate'] * 100
    fig_waste = px.bar(
        waste_cat.sort_values('overpackaged_pct', ascending=False),
        x='category', y='overpackaged_pct',
        color='overpackaged_pct',
        color_continuous_scale=['#1D9E75','#F5A623','#D85A30'],
        title='What % of products ship in an oversized box? (P3)',
        labels={'overpackaged_pct':'% of products shipped in oversized box',
                'category':'Product category'},
        text='overpackaged_pct'
    )
    fig_waste.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_waste.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             coloraxis_showscale=False, height=360)
    st.plotly_chart(fig_waste, use_container_width=True)

    st.markdown("---")
    st.subheader("🕐 When do customers try to return products? (P4)")
    st.markdown(
        "The chart below shows what time of day return attempts happen. "
        "The red bars are outside standard business hours (before 9am and after 6pm). "
        "A large share of returns are attempted when no courier is available to pick up."
    )
    hour_counts = returns_df['return_attempt_hour'].value_counts().sort_index().reset_index()
    hour_counts.columns = ['hour','count']
    hour_counts['period'] = hour_counts['hour'].apply(
        lambda h: 'Outside business hours' if h < 9 or h >= 18 else 'Business hours (9am–6pm)'
    )
    fig_hours = px.bar(
        hour_counts, x='hour', y='count', color='period',
        color_discrete_map={
            'Outside business hours':'#D85A30',
            'Business hours (9am–6pm)':'#378ADD'
        },
        title='When do customers attempt to return items? (P4)',
        labels={'hour':'Hour of day (0 = midnight, 12 = noon)','count':'Number of return attempts',
                'period':'Time period'}
    )
    fig_hours.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=360)
    st.plotly_chart(fig_hours, use_container_width=True)

    after_pct = returns_df['return_attempt_hour'].apply(lambda h: h < 9 or h >= 18).mean() * 100
    st.error(
        f"🔴 **{after_pct:.1f}% of return attempts happen outside business hours.** "
        f"These customers have no way to hand over their return package until the next working day — "
        f"leading to frustration and reduced trust in the platform."
    )

# ── footer ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:12px;color:gray'>"
    "E-Commerce Analytics Platform · Built with Python, XGBoost & Streamlit · "
    "Dataset generated with Faker (en_IN) · 10 problems · 3 ML models · 1 dashboard"
    "</div>",
    unsafe_allow_html=True
)