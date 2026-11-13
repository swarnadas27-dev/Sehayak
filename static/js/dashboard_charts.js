/**
 * SEHAYAK (सहायक) - Teacher Analytics Charts (Plotly.js)
 * Accessible, color-blind friendly data visualizations.
 * Includes:
 * 1. Support Distribution Donut
 * 2. Subject Averages Bar Chart
 * 3. 4-Quadrant Attendance vs. Performance Scatter Plot
 * 4. Feature Contributions (SHAP-Style) Breakdown
 * 5. Student Longitudinal Trajectory Chart
 */

function renderRiskDonut(highCount, moderateCount, onTrackCount, containerId = "risk-donut-chart") {
    const container = document.getElementById(containerId);
    if (!container || typeof Plotly === "undefined") return;

    const totalStudents = highCount + moderateCount + onTrackCount;

    // Ordered to match reference mockup: Green (On-Track) on left, Amber (Guided) at bottom, Red (Priority) on right
    const data = [{
        values: [onTrackCount, moderateCount, highCount],
        labels: ["On-Track", "Guided Support", "Priority Support"],
        type: "pie",
        hole: 0.68,
        sort: false,
        direction: "clockwise",
        rotation: 0,
        marker: {
            colors: ["#059669", "#D97706", "#DC2626"]
        },
        textinfo: "none",
        hoverinfo: "label+value+percent"
    }];

    const layout = {
        showlegend: false,
        height: 220,
        margin: { l: 8, r: 8, t: 8, b: 8 },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        font: { family: "PT Sans, Lexend, sans-serif", size: 12 },
        annotations: [{
            showarrow: false,
            text: `<span style="font-size:32px;font-weight:800;color:#01463C;line-height:1;">${totalStudents}</span><br><span style="font-size:14px;font-weight:600;color:#537D75;line-height:1.4;">Students</span>`,
            x: 0.5,
            y: 0.5
        }]
    };

    const config = { responsive: true, displayModeBar: false };
    Plotly.newPlot(containerId, data, layout, config);
}

function renderSubjectAverages(subjectAvgs, containerId = "subject-bar-chart") {
    const container = document.getElementById(containerId);
    if (!container || typeof Plotly === "undefined") return;

    const subjects = ["Maths", "Science", "English", "Social Science", "Hindi"];
    const keys = ["math", "science", "english", "social", "hindi"];
    const values = keys.map(k => subjectAvgs[k] || 0);

    const data = [{
        x: subjects,
        y: values,
        type: "bar",
        marker: { 
            color: "#2563EB",
            opacity: 0.9,
            line: { color: "#1D4ED8", width: 1.5 }
        },
        text: values.map(v => `${v}%`),
        textposition: "outside",
        cliponaxis: false,
        hovertemplate: "<b>%{x}</b><br>Average: %{y:.1f}%<br>Benchmark: 35%<extra></extra>"
    }];

    const layout = {
        height: 230,
        margin: { l: 38, r: 15, t: 25, b: 35 },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        yaxis: { 
            range: [0, 100], 
            title: { text: "Score (%)", font: { size: 10, color: "#537D75" } },
            gridcolor: "#EADBC8",
            zeroline: false,
            tickfont: { size: 10, color: "#537D75" }
        },
        xaxis: {
            tickfont: { size: 11, color: "#01463C", family: "inherit", weight: 600 }
        },
        font: { family: "PT Sans, Lexend, sans-serif", size: 11 },
        shapes: [{
            type: "line",
            x0: -0.5,
            x1: 4.5,
            y0: 35,
            y1: 35,
            line: { color: "#DC2626", width: 1.5, dash: "dot" }
        }],
        annotations: [{
            x: 4.5,
            y: 42,
            xref: "x",
            yref: "y",
            text: "35% Benchmark",
            showarrow: false,
            xanchor: "right",
            font: { color: "#DC2626", size: 10, weight: "bold" },
            bgcolor: "rgba(254, 242, 242, 0.9)",
            bordercolor: "#FCA5A5",
            borderwidth: 1,
            borderpad: 2
        }]
    };

    const config = { responsive: true, displayModeBar: false };
    Plotly.newPlot(containerId, data, layout, config);
}

function renderQuadrantScatter(studentsData, containerId = "quadrant-scatter-chart") {
    const container = document.getElementById(containerId);
    if (!container || typeof Plotly === "undefined" || !studentsData || studentsData.length === 0) return;

    // Group students by support risk level for distinct colors
    const groups = {
        HIGH: { x: [], y: [], text: [], ids: [] },
        MODERATE: { x: [], y: [], text: [], ids: [] },
        LOW: { x: [], y: [], text: [], ids: [] }
    };

    studentsData.forEach(s => {
        const lvl = s.risk_level || "LOW";
        const target = groups[lvl] || groups.LOW;
        target.x.push(s.attendance_rate);
        target.y.push(s.overall_avg);
        target.ids.push(s.student_id);
        target.text.push(
            `<b>${s.name}</b> (${s.student_id})<br>` +
            `Attendance: ${s.attendance_rate.toFixed(1)}%<br>` +
            `Overall Marks: ${s.overall_avg.toFixed(1)}%<br>` +
            `Profile: ${s.archetype || 'General'}<br>` +
            `Status: ${s.risk_level}`
        );
    });

    const traces = [
        {
            x: groups.HIGH.x,
            y: groups.HIGH.y,
            text: groups.HIGH.text,
            customdata: groups.HIGH.ids,
            mode: "markers",
            name: "Priority Support",
            type: "scatter",
            marker: { size: 10, color: "#DC2626", opacity: 0.85, line: { width: 1, color: "#991B1B" } },
            hoverinfo: "text"
        },
        {
            x: groups.MODERATE.x,
            y: groups.MODERATE.y,
            text: groups.MODERATE.text,
            customdata: groups.MODERATE.ids,
            mode: "markers",
            name: "Guided Support",
            type: "scatter",
            marker: { size: 9, color: "#D97706", opacity: 0.85, line: { width: 1, color: "#92400E" } },
            hoverinfo: "text"
        },
        {
            x: groups.LOW.x,
            y: groups.LOW.y,
            text: groups.LOW.text,
            customdata: groups.LOW.ids,
            mode: "markers",
            name: "On-Track Progress",
            type: "scatter",
            marker: { size: 8, color: "#059669", opacity: 0.85, line: { width: 1, color: "#065F46" } },
            hoverinfo: "text"
        }
    ];

    const layout = {
        height: 380,
        margin: { l: 50, r: 30, t: 30, b: 50 },
        paper_bgcolor: "transparent",
        plot_bgcolor: "rgba(0,0,0,0.02)",
        xaxis: {
            title: "Attendance Rate (%)",
            range: [40, 102],
            gridcolor: "rgba(0,0,0,0.06)"
        },
        yaxis: {
            title: "Academic Performance (%)",
            range: [20, 102],
            gridcolor: "rgba(0,0,0,0.06)"
        },
        font: { family: "Lexend, sans-serif", size: 11 },
        legend: { orientation: "h", y: 1.15, x: 0.1 },
        shapes: [
            // Vertical 75% Attendance Benchmark
            {
                type: "line",
                x0: 75, x1: 75,
                y0: 20, y1: 100,
                line: { color: "#D97706", width: 2, dash: "dash" }
            },
            // Horizontal 50% Benchmark
            {
                type: "line",
                x0: 40, x1: 100,
                y0: 50, y1: 50,
                line: { color: "#2563EB", width: 2, dash: "dash" }
            }
        ],
        annotations: [
            {
                x: 88, y: 35,
                text: "<b>Quadrant 2: Learning / Dyslexia Gap</b><br>(High Attendance + Low Marks)",
                showarrow: false,
                font: { size: 10, color: "#92400E" },
                bgcolor: "rgba(254, 243, 199, 0.6)",
                bordercolor: "#FCD34D",
                borderwidth: 1
            },
            {
                x: 58, y: 35,
                text: "<b>Quadrant 3: Attendance Deficit</b><br>(Low Attendance + Low Marks)",
                showarrow: false,
                font: { size: 10, color: "#991B1B" },
                bgcolor: "rgba(254, 226, 226, 0.6)",
                bordercolor: "#FCA5A5",
                borderwidth: 1
            },
            {
                x: 88, y: 85,
                text: "<b>Quadrant 1: Mastery</b><br>(High Attendance + High Marks)",
                showarrow: false,
                font: { size: 10, color: "#065F46" },
                bgcolor: "rgba(209, 250, 229, 0.6)",
                bordercolor: "#6EE7B7",
                borderwidth: 1
            },
            {
                x: 58, y: 85,
                text: "<b>Quadrant 4: Independent Learner</b><br>(Low Attendance + High Marks)",
                showarrow: false,
                font: { size: 10, color: "#4338CA" },
                bgcolor: "rgba(224, 231, 255, 0.6)",
                bordercolor: "#A5B4FC",
                borderwidth: 1
            }
        ]
    };

    const config = { responsive: true, displayModeBar: false };
    Plotly.newPlot(containerId, traces, layout, config);

    // Optional click to navigate to student details
    container.on("plotly_click", function (data) {
        if (data.points && data.points.length > 0) {
            const stuId = data.points[0].customdata;
            if (stuId) {
                window.location.href = `/student/${stuId}`;
            }
        }
    });
}

function renderFeatureContributionsChart(factors, containerId = "feature-contrib-chart") {
    const container = document.getElementById(containerId);
    if (!container || typeof Plotly === "undefined" || !factors || factors.length === 0) return;

    const labels = factors.map(f => f.name);
    const values = factors.map(f => f.impact); // positive = risk, negative = protective
    const colors = values.map(v => v > 0 ? "#DC2626" : "#059669");

    const data = [{
        y: labels,
        x: values,
        type: "bar",
        orientation: "h",
        marker: { color: colors, opacity: 0.85 },
        text: values.map(v => v > 0 ? `+${v.toFixed(1)}% Risk` : `${v.toFixed(1)}% Protective`),
        textposition: "outside"
    }];

    const layout = {
        height: 250,
        margin: { l: 150, r: 80, t: 20, b: 30 },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        xaxis: {
            title: "Contribution Impact (%)",
            zeroline: true,
            zerolinecolor: "#374151",
            zerolinewidth: 2
        },
        font: { family: "Lexend, sans-serif", size: 11 }
    };

    const config = { responsive: true, displayModeBar: false };
    Plotly.newPlot(containerId, data, layout, config);
}

function renderStudentTrend(fa1, sa1, fa2, sa2, containerId = "student-trend-chart") {
    const container = document.getElementById(containerId);
    if (!container || typeof Plotly === "undefined") return;

    const terms = ["FA 1", "SA 1 (Term 1)", "FA 2", "SA 2 (Term 2)"];
    const values = [fa1, sa1, fa2, sa2];

    const data = [{
        x: terms,
        y: values,
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#2563EB", width: 3 },
        marker: { size: 9, color: "#1D4ED8" },
        text: values.map(v => `${v}%`),
        textposition: "top center"
    }];

    const layout = {
        height: 260,
        margin: { l: 40, r: 20, t: 20, b: 35 },
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        yaxis: { range: [0, 100], title: "Marks (%)" },
        font: { family: "Lexend, sans-serif", size: 11 }
    };

    const config = { responsive: true, displayModeBar: false };
    Plotly.newPlot(containerId, data, layout, config);
}
