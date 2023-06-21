require "json"

#
# Regenerate:
#
# Scrape and save the glossary sources.
# Requires the executables "poetry", "scrapy", "jq" and "sponge".
#
module Export
  VERSION      = "0.1.0"
  DATASETS_DIR = Path["../../../datasets/"]

  GLOSSARY_SPIDERS = `poetry run scrapy list`.split.select { |s| s.includes?("glossar") }
  DATALINKS        = Hash(String, String).from_json(File.read("../../config/datalinks.json"))

  GLOSSARY_SPIDERS.each do |spider|
    output_path = DATASETS_DIR.join(DATALINKS[spider])

    puts "Exporting #{spider}\n       to #{output_path}...\n\n"
    `poetry run scrapy crawl --nolog --overwrite-output #{output_path} #{spider}`
    `jq . #{output_path} | sponge #{output_path}`
  end
end
