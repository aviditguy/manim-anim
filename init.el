(require 'package)

(setq package-archives '(("melpa" . "https://melpa.org/packages/")
                         ("gnu" . "https://elpa.gnu.org/packages/")))

(package-initialize)

(unless package-archive-contents (package-refresh-contents))

(unless (package-installed-p 'use-package)
  (package-install 'use-package))

(require 'use-package)

(setq use-package-always-ensure t)  ;; auto-install packages

;; Doom themes
(use-package doom-themes)


;; Set Font
(set-face-attribute 'default nil :font "Iosevka ExtraLight Extended" :height 115)



;; ────────────────────────────────────────────────────────────────────────────────────────────────────
;; Cycle through Themes
;; ────────────────────────────────────────────────────────────────────────────────────────────────────
(defvar my/theme-state
  '(:themes 
    (doom-material-dark
     doom-1337
     doom-dark+)
    :index 0))

(defun my/get-themes ()
  (plist-get my/theme-state :themes))

(defun my/get-theme-index ()
  (plist-get my/theme-state :index))

(defun my/get-current-theme ()
  (nth (my/get-theme-index)
       (plist-get my/theme-state :themes)))

(defun my/update-theme-index ()
  (setq my/theme-state
	(plist-put my/theme-state
		   :index (mod (1+ (my/get-theme-index)) (length (my/get-themes))))))

(defun my/cycle-theme ()
  (interactive)
  (mapc #'disable-theme custom-enabled-themes)
  (load-theme (my/get-current-theme) t)
  (load-theme (my/get-current-theme) t)
  
  (message "Theme [%d/%d]: %s"
	   (my/get-theme-index)
	   (1- (length (my/get-themes)))
	   (my/get-current-theme))

  (my/update-theme-index))

;; Ye ek baar run karna hai
(my/cycle-theme)

(global-set-key (kbd "<f5>") #'my/cycle-theme)


;; ────────────────────────────────────────────────────────────────────────────────────────────────────
;; Terminal Toggle
;; ────────────────────────────────────────────────────────────────────────────────────────────────────
(defvar my/term-state
  '(:name "*my-terminal*"
	  :active nil
	  :below t)
  "State for my terminal toggle system.")

(defun my/term-name ()
  "Helper function to get name from my/term-state"
  (plist-get my/term-state :name))

(defun my/term-active ()
  "Helper function to extract active flag from my/term-state"
  (plist-get my/term-state :active))

(defun my/term-buffer ()
  "Helper function to get the my/term-state :name buffer from buffer list"
  (get-buffer (my/term-name)))

(defun my/term-create ()
  "Create ansi-term in backgrond if does not exists"
  (unless (my/term-buffer)
    (save-window-excursion
      (let ((buf (ansi-term (getenv "SHELL"))))
	(with-current-buffer buf
	  (rename-buffer (my/term-name) t))))))

(defun my/term-show ()
  "Create and show terminal in split-window"
  (my/term-create)
  ;; only show if not already active
  (unless (my/term-active)
    (let ((win (if (plist-get my/term-state :below)
		   (split-window-below -15)
		 (split-window-right -100))))      
      (set-window-buffer win (my/term-buffer))
      (select-window win)
      (setq my/term-state (plist-put my/term-state :active t)))))

(defun my/term-hide ()
  "Hide the terminal by deleting the split-window"
  (when-let ((win (get-buffer-window (my/term-buffer))))
    (delete-window win)
    (setq my/term-state (plist-put my/term-state :active nil))))

(defun my/term-toggle ()
  "Toggle terminal if no terminal first create it and then show/hide"
  (interactive)

  (if (my/term-active)
      (my/term-hide)
    (my/term-show)))

(defun my/term-toggle-move ()
  "Move terminal toggle from bottom <-> right"
  (interactive)

  (setq my/term-state
	(plist-put my/term-state :below
		   (not (plist-get my/term-state :below))))
  
  (if (my/term-active)
      (progn
	(my/term-hide)
	(my/term-show))
    (my/term-show)))

(global-set-key (kbd "C-`") #'my/term-toggle)
(global-set-key (kbd "C-M-`") #'my/term-toggle-move)











(defun my/term-send (cmd)
  (my/term-show)
  (let* ((buf  (my/term-buffer))
	 (proc (and buf (get-buffer-process buf))))
    (unless proc
      (error "No running terminal process"))
    (process-send-string proc (concat cmd "\n"))))

(defun my/extract-org-src-block ()
  (interactive)
  (let ((element (org-element-context)))
    (unless (eq (org-element-type element) 'src-block)
      (error "Point is not inside an Org src block"))

    (let* ((lang   (org-element-property :language element))
	   (body   (org-element-property :value element))
	   (result (list :lang lang :body body)))
      result)))

(defun my/run-org-src-block ()
  (interactive)
  (let* ((data (my/extract-org-src-block))
	 (lang (plist-get data :lang))
	 (body (plist-get data :body)))

    (cond
     ((string= lang "shell")
      (my/term-send body))

     (t
      (message "not handled")))))
