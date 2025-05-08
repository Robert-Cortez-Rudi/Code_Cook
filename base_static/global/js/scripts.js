function scope() {
    const forms = document.querySelectorAll(".form-delete")

    for (const form of forms) {
        if (form) {
            form.addEventListener("submit", (eve) => {
                eve.preventDefault()
                
                const confirmed = confirm("Are you sure?")
    
                if (confirmed) {
                    form.submit()
                }
            })
        }
    }
}

scope()
