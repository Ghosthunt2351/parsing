from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from vacancy_parser.spiders.hh import HhSpider
import sys

if __name__ == '__main__':
  configure_logging()
  settings = get_project_settings()
  runner = CrawlerRunner(settings)
  '''Ввод вакансии для поиска реализован двумя способами.
  Основной ввод через инпут, при запуске из IDE.
  Второй вариант (закомментирован) для использования через терминал.'''
  search = input('Введите искомую вакансию: ')
  # if len(sys.argv) != 1:
  #     search = ' '.join(sys.argv[1:])
  runner.crawl(HhSpider, search=search)

  d = runner.join()
  d.addBoth(lambda _: reactor.stop())
  reactor.run()
  