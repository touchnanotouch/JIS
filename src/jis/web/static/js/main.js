document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const sidebarToggle = document.querySelector(".sidebar__toggle");
    const toggleIcon = document.querySelector(".toggle-icon");

    const isCollapsed = localStorage.getItem("sidebarCollapsed") === "true";

    document.documentElement.style.setProperty(
        "--sidebar-current-width", 
        isCollapsed ? "var(--sidebar-width-collapsed)" : "var(--sidebar-width)"
    );

    if (isCollapsed) {
        sidebar.classList.add("sidebar--collapsed");
        updateToggleIcon(true);
    }

    sidebarToggle.addEventListener("click", function() {
        const isNowCollapsed = !sidebar.classList.contains("sidebar--collapsed");

        document.documentElement.style.setProperty(
            "--sidebar-current-width",
            isNowCollapsed ? "var(--sidebar-width-collapsed)" : "var(--sidebar-width)"
        );

        if (isNowCollapsed) {
            sidebar.classList.add("sidebar--collapsed");
        } else {
            sidebar.classList.remove("sidebar--collapsed");
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

    sidebar.style.visibility = "visible";
});
