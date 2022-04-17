using System;
using System.Collections.Generic;

namespace thumbnailService.Entities.Sql
{
    public partial class Jobs
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public Guid? Modelid { get; set; }
        public Guid? Statusid { get; set; }

        public virtual Jobstatus Status { get; set; }
    }
}
