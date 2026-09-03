/* =========================================================
   Owajid AI Trading Assistant
   Application Logic
========================================================= */

"use strict";


/* =========================================================
   APP STATE
========================================================= */

const AppState = {
    market: "XAUUSD",
    timeframe: "15M",
    connected: false,
    analyzing: false
};


/* =========================================================
   DOM HELPERS
========================================================= */

function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}


/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    initializeTimeframes();
    initializeChartTimeframes();
    initializeRefreshButton();
    initializeNavigation();
    initializeKeyboardShortcuts();

    updateSystemStatus();

});


/* =========================================================
   TIMEFRAME BUTTONS
========================================================= */

function initializeTimeframes() {

    const buttons = $$(".timeframes button");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            const timeframe = button.textContent.trim();

            AppState.timeframe = timeframe;

            buttons.forEach(item => {
                item.classList.remove("selected");
            });

            button.classList.add("selected");

            updateChartTimeframe(timeframe);

            showTemporaryStatus(
                `Timeframe changed to ${timeframe}`
            );

        });

    });

}


/* =========================================================
   CHART TIMEFRAME BUTTONS
========================================================= */

function initializeChartTimeframes() {

    const buttons = $$(".chart-time");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            const timeframe = button.textContent.trim();

            AppState.timeframe = timeframe;

            buttons.forEach(item => {
                item.classList.remove("active");
            });

            button.classList.add("active");

            syncMainTimeframe(timeframe);

            showTemporaryStatus(
                `Chart timeframe: ${timeframe}`
            );

        });

    });

}


/* =========================================================
   SYNC TIMEFRAME UI
========================================================= */

function syncMainTimeframe(timeframe) {

    const buttons = $$(".timeframes button");

    buttons.forEach(button => {

        if (button.textContent.trim() === timeframe) {
            button.classList.add("selected");
        } else {
            button.classList.remove("selected");
        }

    });

}


/* =========================================================
   CHART UPDATE
========================================================= */

function updateChartTimeframe(timeframe) {

    const chartButtons = $$(".chart-time");

    chartButtons.forEach(button => {

        if (button.textContent.trim() === timeframe) {
            button.classList.add("active");
        } else {
            button.classList.remove("active");
        }

    });

}


/* =========================================================
   REFRESH ANALYSIS
========================================================= */

function initializeRefreshButton() {

    const button = $(".refresh-button");

    if (!button) return;

    button.addEventListener("click", async () => {

        if (AppState.analyzing) {
            return;
        }

        AppState.analyzing = true;

        const originalText = button.innerHTML;

        button.innerHTML = `
            <span>↻</span>
            Analyzing...
        `;

        button.style.opacity = "0.7";

        updateAnalysisState("Analyzing market...");

        await wait(1200);

        /*
         * IMPORTANT:
         * No fake BUY/SELL signal is generated here.
         *
         * Real market data + technical engine + AI
         * will be connected in later stages.
         */

        updateAnalysisState(
            "Market data connection required"
        );

        button.innerHTML = originalText;

        button.style.opacity = "1";

        AppState.analyzing = false;

    });

}


/* =========================================================
   ANALYSIS STATUS
========================================================= */

function updateAnalysisState(message) {

    const chartStatus = $(".chart-center span");

    if (chartStatus) {
        chartStatus.textContent = message;
    }

}


/* =========================================================
   SYSTEM STATUS
========================================================= */

function updateSystemStatus() {

    /*
     * Frontend is online.
     * Real market connection will be added later.
     */

    AppState.connected = false;

}


/* =========================================================
   NAVIGATION
========================================================= */

function initializeNavigation() {

    const navigationItems = $$(".nav-item");

    navigationItems.forEach(item => {

        item.addEventListener("click", () => {

            navigationItems.forEach(nav => {
                nav.classList.remove("active");
            });

            item.classList.add("active");

            const name =
                item.textContent.trim();

            showTemporaryStatus(
                `${name} selected`
            );

        });

    });

}


/* =========================================================
   TEMPORARY STATUS MESSAGE
========================================================= */

function showTemporaryStatus(message) {

    let notification =
        $(".temporary-notification");

    if (!notification) {

        notification =
            document.createElement("div");

        notification.className =
            "temporary-notification";

        notification.style.position = "fixed";
        notification.style.bottom = "22px";
        notification.style.right = "22px";
        notification.style.zIndex = "9999";
        notification.style.padding = "11px 15px";
        notification.style.background = "#151b25";
        notification.style.border = "1px solid #2a3340";
        notification.style.borderRadius = "10px";
        notification.style.color = "#f4f7fb";
        notification.style.fontSize = "11px";
        notification.style.boxShadow =
            "0 12px 35px rgba(0,0,0,0.35)";
        notification.style.transition =
            "opacity 0.25s ease";

        document.body.appendChild(notification);
    }

    notification.textContent = message;
    notification.style.opacity = "1";

    clearTimeout(
        notification.hideTimer
    );

    notification.hideTimer =
        setTimeout(() => {

            notification.style.opacity = "0";

        }, 1800);

}


/* =========================================================
   KEYBOARD SHORTCUTS
========================================================= */

function initializeKeyboardShortcuts() {

    document.addEventListener("keydown", event => {

        /*
         * R = Refresh analysis
         */

        if (
            event.key.toLowerCase() === "r" &&
            !isTyping()
        ) {

            const button =
                $(".refresh-button");

            if (button) {
                button.click();
            }

        }

    });

}


/* =========================================================
   INPUT CHECK
========================================================= */

function isTyping() {

    const active =
        document.activeElement;

    if (!active) return false;

    const tag =
        active.tagName.toLowerCase();

    return (
        tag === "input" ||
        tag === "textarea" ||
        tag === "select"
    );

}


/* =========================================================
   UTILITY
========================================================= */

function wait(milliseconds) {

    return new Promise(resolve => {

        setTimeout(
            resolve,
            milliseconds
        );

    });

}


/* =========================================================
   FUTURE API PLACEHOLDERS
========================================================= */

/*
   Later stages will add:

   1. Real market data
   2. Candlestick chart
   3. Market structure detection
   4. BOS / CHOCH
   5. Liquidity sweep
   6. FVG
   7. Order Block
   8. Multi-timeframe engine
   9. AI analysis
   10. Signal scoring
   11. Risk management
   12. Backtesting

   No API keys should ever be placed
   directly inside this frontend file.
*/


console.log(
    "Owajid AI Trading Assistant loaded."
);
