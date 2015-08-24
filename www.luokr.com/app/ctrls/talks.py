#coding=utf-8

from basic import BasicCtrl

class TalksCtrl(BasicCtrl):
    def get(self, _ext = '.json'):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        cur_talks = self.dbase('talks').cursor()
        cur_talks.execute('select talk_id, user_id, user_name, talk_text, talk_ctms from talks \
                where post_id=? and talk_rank>=? order by talk_id asc limit ? offset ?',
                (self.input('ptid', ''), self.get_runtime_conf('posts_talks_min_rank'), pager['qnty'], (pager['page']-1)*pager['qnty']))
        # talks = cur_talks.fetchall()
        talks = self.utils().sqlite_rows(cur_talks)
        cur_talks.close()

        if talks:
            pager['lgth'] = len(talks)

        self.flash(1, {'dat': {'talks': talks, 'pager': pager}}, _ext)
