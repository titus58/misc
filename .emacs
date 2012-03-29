;(require 'tramp)

(global-set-key (kbd "M-1") 'compile)


(add-to-list 'load-path "~/.emacs.d/elisp")
;(require 'buffer-move)

(defun swap-buffers-in-windows () ;from stackoverflow
  "Put the buffer from the selected window in next window, and vice versa"
  (interactive)
  (let* ((this (selected-window))
	 (other (next-window))
     (this-buffer (window-buffer this))
     (other-buffer (window-buffer other)))
    (set-window-buffer other this-buffer)
    (set-window-buffer this other-buffer)
    )
  )

(global-set-key (kbd "C-x t") 'swap-buffers-in-windows)

(desktop-save-mode 1)

(require 'magit)