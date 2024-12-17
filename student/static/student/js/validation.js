// Validation and Alert Utilities
const SMS = {
    // Show a success toast message
    toast: (message, type = 'success') => {
        Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true
        }).fire({
            icon: type,
            title: message
        });
    },
    
    // Show a confirmation dialog
    confirm: async (title, text = '', type = 'warning') => {
        const result = await Swal.fire({
            title: title,
            text: text,
            icon: type,
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            reverseButtons: true,
            customClass: {
                confirmButton: 'btn btn-primary ms-2',
                cancelButton: 'btn btn-outline-secondary'
            },
            buttonsStyling: false
        });
        return result.isConfirmed;
    },
    
    // Show an error message
    error: (title, text = '') => {
        Swal.fire({
            title: title,
            text: text,
            icon: 'error',
            customClass: {
                confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
        });
    },
    
    // Form validation helper
    validateForm: (formElement) => {
        const form = formElement instanceof HTMLFormElement ? formElement : document.querySelector(formElement);
        if (!form) return true;
        
        let isValid = true;
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Reset previous validation state
            input.classList.remove('is-invalid');
            const feedbackElement = input.nextElementSibling;
            if (feedbackElement?.classList.contains('invalid-feedback')) {
                feedbackElement.remove();
            }
            
            // Check validity
            if (input.hasAttribute('required') && !input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                feedback.textContent = `${input.name || 'This field'} is required`;
                input.parentNode.insertBefore(feedback, input.nextSibling);
            }
            
            // Email validation
            if (input.type === 'email' && input.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(input.value)) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'Please enter a valid email address';
                    input.parentNode.insertBefore(feedback, input.nextSibling);
                }
            }
            
            // Password validation
            if (input.type === 'password' && input.value && input.minLength) {
                if (input.value.length < input.minLength) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = `Password must be at least ${input.minLength} characters`;
                    input.parentNode.insertBefore(feedback, input.nextSibling);
                }
            }
        });
        
        return isValid;
    },
    
    // Handle form submission with validation
    handleFormSubmit: async (formElement, options = {}) => {
        const {
            confirmMessage = 'Are you sure you want to submit this form?',
            successMessage = 'Form submitted successfully!',
            errorMessage = 'An error occurred while submitting the form.',
            validate = true,
            confirm = true
        } = options;
        
        // Validate form if requested
        if (validate && !SMS.validateForm(formElement)) {
            return false;
        }
        
        // Show confirmation if requested
        if (confirm) {
            const confirmed = await SMS.confirm('Confirm Submission', confirmMessage);
            if (!confirmed) return false;
        }
        
        try {
            // Submit form
            const form = formElement instanceof HTMLFormElement ? formElement : document.querySelector(formElement);
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                SMS.toast(successMessage);
                return true;
            } else {
                throw new Error(await response.text());
            }
        } catch (error) {
            SMS.error('Error', errorMessage);
            console.error('Form submission error:', error);
            return false;
        }
    }
};
