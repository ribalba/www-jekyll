# Liquid filter that turns a site path into a human readable file size, so
# download links can say how big the file is.
#
#   {{ "/assets/2024/pdf/slides-3.pdf" | file_size }}  =>  "1.2 MB"
#
# The size is read from the source folder at build time, so it never goes
# stale. External links and missing files give an empty string, and a
# missing local file also prints a build warning.
module HotCarbon
  module FileSizeFilter
    def file_size(path)
      return "" if path.nil?
      path = path.to_s.strip
      return "" if path.empty? || path.match?(%r{\A[a-z]+:|\A//}i)

      site = @context.registers[:site]
      local = path.split(/[?#]/).first
      file = File.join(site.source, local)
      unless File.file?(file)
        Jekyll.logger.warn "file_size:", "#{local} not found"
        return ""
      end

      bytes = File.size(file)
      if bytes >= 1_000_000
        format("%.1f MB", bytes / 1_000_000.0)
      else
        format("%d kB", [(bytes / 1000.0).round, 1].max)
      end
    end
  end
end

Liquid::Template.register_filter(HotCarbon::FileSizeFilter)
