document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar-wrapper");
    const sidebarToggle = document.querySelector(".sidebar-toggle");
    const toggleIcon = document.querySelector(".toggle-icon");

    const isCollapsed = localStorage.getItem("sidebarCollapsed") === "true";

    document.documentElement.style.setProperty(
        "--sidebar-current-width", 
        isCollapsed ? "var(--sidebar-width-collapsed)" : "var(--sidebar-width)"
    );

    if (isCollapsed) {
        sidebar.classList.add("collapsed");
        updateToggleIcon(true);
    }

    sidebarToggle.addEventListener("click", function() {
        const isNowCollapsed = !sidebar.classList.contains("collapsed");

        document.documentElement.style.setProperty(
            "--sidebar-current-width",
            isNowCollapsed ? "var(--sidebar-width-collapsed)" : "var(--sidebar-width)"
        );

        if (isNowCollapsed) {
            sidebar.classList.add("collapsed");
        } else {
            sidebar.classList.remove("collapsed");
        }
        
        localStorage.setItem("sidebarCollapsed", isNowCollapsed);
        updateToggleIcon(isNowCollapsed);
    });
    
    function updateToggleIcon(isCollapsed) {
        if (toggleIcon) {
            toggleIcon.className = isCollapsed ? 
                "fas fa-chevron-right toggle-icon" : 
                "fas fa-chevron-left toggle-icon";
        }
    }
});
