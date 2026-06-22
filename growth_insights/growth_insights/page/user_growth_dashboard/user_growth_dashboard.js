frappe.pages["user-growth-dashboard"].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Zhige Energy Operations Dashboard"),
        single_column: true
    });

    page.main.addClass("growth-dashboard-shell");
    page.main.html(`
        <div class="growth-dashboard">
            <section class="growth-hero">
                <div>
                    <p class="growth-kicker">${__("Battery Swapping Command Center")}</p>
                    <h1>${__("Zhige Energy Operations Dashboard")}</h1>
                    <p class="growth-period"></p>
                </div>
                <div class="growth-clock">
                    <span>${__("Live Operations Snapshot")}</span>
                    <strong></strong>
                </div>
            </section>

            <section class="growth-kpis">
                ${["active_customers", "active_mrr", "net_new_mrr", "logo_churn_rate"].map((key) => `
                    <article class="growth-kpi" data-kpi="${key}">
                        <span></span>
                        <strong>--</strong>
                        <em></em>
                    </article>
                `).join("")}
            </section>

            <section class="growth-main-grid">
                <article class="growth-panel growth-panel-wide">
                    <header>
                        <h2>${__("Monthly Service Growth")}</h2>
                        <span>${__("New service accounts, churn, and net revenue")}</span>
                    </header>
                    <div id="growth-monthly-chart" class="growth-chart"></div>
                </article>
                <article class="growth-panel">
                    <header>
                        <h2>${__("Operating Territory Distribution")}</h2>
                        <span>${__("Active service revenue by region")}</span>
                    </header>
                    <div class="growth-bars" data-list="regions"></div>
                </article>
            </section>

            <section class="growth-lower-grid">
                <article class="growth-panel">
                    <header>
                        <h2>${__("Acquisition Mix")}</h2>
                        <span>${__("New riders, fleets, and stations by channel")}</span>
                    </header>
                    <div class="growth-bars compact" data-list="channels"></div>
                </article>
                <article class="growth-panel">
                    <header>
                        <h2>${__("Service Object Value")}</h2>
                        <span>${__("Revenue by rider, fleet, and station account")}</span>
                    </header>
                    <div class="growth-bars compact" data-list="segments"></div>
                </article>
                <article class="growth-panel">
                    <header>
                        <h2>${__("Recent Lifecycle Events")}</h2>
                        <span>${__("Latest movement")}</span>
                    </header>
                    <div class="growth-events"></div>
                </article>
            </section>
        </div>
    `);

    render_dashboard(page);
};

async function render_dashboard(page) {
    const response = await frappe.call({
        method: "growth_insights.growth_insights.page.user_growth_dashboard.user_growth_dashboard.get_dashboard_data"
    });
    const data = response.message || {};
    const root = page.main.find(".growth-dashboard");

    root.find(".growth-period").text(`${data.start_date || ""} - ${data.end_date || ""}`);
    root.find(".growth-clock strong").text(frappe.datetime.str_to_user(frappe.datetime.now_datetime()));

    const kpis = {
        active_customers: [__("Active Service Accounts"), data.summary?.active_customers || 0, __("Riders, fleets, and stations retained")],
        active_mrr: [__("Active Service Revenue"), format_currency(data.summary?.active_mrr || 0), __("Latest operating account state")],
        net_new_mrr: [__("Net New Revenue"), format_currency(data.summary?.net_new_mrr || 0), __("Signup + expansion - churn")],
        logo_churn_rate: [__("Account Churn"), `${flt(data.summary?.logo_churn_rate || 0, 1)}%`, __("Service loss pressure")]
    };

    Object.entries(kpis).forEach(([key, value]) => {
        const card = root.find(`[data-kpi="${key}"]`);
        card.find("span").text(value[0]);
        card.find("strong").text(value[1]);
        card.find("em").text(value[2]);
    });

    render_monthly_chart(data.monthly || []);
    render_bars(root.find('[data-list="regions"]'), data.regions || [], "region", "mrr", "active_customers");
    render_bars(root.find('[data-list="channels"]'), data.channels || [], "channel", "new_customers", "mrr");
    render_bars(root.find('[data-list="segments"]'), data.segments || [], "segment", "mrr", "active_customers");
    render_events(root.find(".growth-events"), data.recent_events || []);
    bind_dashboard_interactions(root, data.recent_events || []);
}

function render_monthly_chart(rows) {
    const labels = rows.map((item) => item.month);
    const chart_data = {
        labels,
        datasets: [
            { name: __("New Accounts"), chartType: "bar", values: rows.map((item) => item.new_customers || 0) },
            { name: __("Churn"), chartType: "bar", values: rows.map((item) => item.churned_customers || 0) },
            { name: __("Net MRR"), chartType: "line", values: rows.map((item) => item.net_mrr || 0) }
        ]
    };

    new frappe.Chart("#growth-monthly-chart", {
        data: chart_data,
        type: "axis-mixed",
        height: 280,
        colors: ["#4ade80", "#fb7185", "#38bdf8"],
        axisOptions: { xIsSeries: true },
        barOptions: { stacked: false }
    });
}

function render_bars(container, rows, label_key, value_key, sub_key) {
    const max = Math.max(...rows.map((item) => Number(item[value_key] || 0)), 1);
    container.html(rows.slice(0, 7).map((item) => {
        const width = Math.max((Number(item[value_key] || 0) / max) * 100, 4);
        const value = value_key.includes("mrr") ? format_currency(item[value_key] || 0) : item[value_key] || 0;
        const sub = sub_key.includes("mrr") ? format_currency(item[sub_key] || 0) : `${item[sub_key] || 0} ${__("accounts")}`;
        return `
            <div class="growth-bar-row">
                <div class="growth-bar-label">
                    <strong>${frappe.utils.escape_html(item[label_key] || __("Unknown"))}</strong>
                    <span>${value} · ${sub}</span>
                </div>
                <div class="growth-bar-track"><i style="width:${width}%"></i></div>
            </div>
        `;
    }).join("") || `<p class="growth-empty">${__("No data yet")}</p>`);
}

function render_events(container, events) {
    container.html(events.slice(0, 8).map((event) => `
        <div class="growth-event" data-event-type="${frappe.utils.escape_html(event.event_type || "")}">
            <span class="growth-event-type ${String(event.event_type || "").toLowerCase()}">${frappe.utils.escape_html(event.event_type || "")}</span>
            <div>
                <strong>${frappe.utils.escape_html(event.customer_name || "")}</strong>
                <small>${frappe.datetime.str_to_user(event.event_date)} · ${frappe.utils.escape_html(event.region || "")} · ${format_currency(event.mrr || 0)}</small>
            </div>
        </div>
    `).join("") || `<p class="growth-empty">${__("No lifecycle events yet")}</p>`);
}

function bind_dashboard_interactions(root, events) {
    const filter_map = {
        active_customers: "",
        active_mrr: "",
        net_new_mrr: "Expansion",
        logo_churn_rate: "Churn"
    };

    root.find(".growth-kpi").on("click", function() {
        const key = $(this).data("kpi");
        const event_type = filter_map[key] || "";
        root.find(".growth-kpi").removeClass("is-selected");
        $(this).addClass("is-selected");
        const filtered = event_type ? events.filter((event) => event.event_type === event_type) : events;
        render_events(root.find(".growth-events"), filtered.length ? filtered : events);
    });

    root.find(".growth-bars").on("click", ".growth-bar-row", function() {
        $(this).closest(".growth-bars").find(".growth-bar-row").removeClass("is-selected");
        $(this).addClass("is-selected");
    });

    root.find(".growth-events").on("click", ".growth-event", function() {
        root.find(".growth-event").removeClass("is-selected");
        $(this).addClass("is-selected");
    });
}
